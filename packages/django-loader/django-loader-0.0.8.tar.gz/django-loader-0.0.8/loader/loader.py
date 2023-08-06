# ******************************************************************************
#
# django-loader, a configuration and secret loader for Django
#
# loader.py:  main loader functions
#
# Copyright (C) 2021 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************
#
"""Load Django settings.

Load Django settings from defaults, files, or the environment, in that
order.
"""

import json
import os
import sys
import types
import warnings
from pathlib import Path

import bespon
import toml
from django.core.exceptions import ImproperlyConfigured
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError


def generate_secret_key():
    """Generate a secret key for a Django app.

    Generate a secret key for a Django app, using
    ``django.core.management.utils.get_random_secret_key``.

    Returns
    -------
    string
        A random secret key.
    """
    from django.core.management.utils import get_random_secret_key

    return get_random_secret_key()


def load_secrets(fn=".env", prefix="DJANGO_ENV_", **kwargs):
    """Load a list of configuration variables.

    Return a dictionary of configuration variables, as loaded from a
    configuration file or the environment.  Values passed in as
    ``args`` or as the value in ``kwargs`` will be used as the
    configuration variable's default value if one is not found in the
    configuration file or environment.

    Parameters
    ----------
    fn : string, default=".env"
        Configuration filename, defaults to ``.env``.  May be in TOML,
        JSON, YAML, or BespON formats.  Formats will be attempted in this
        order.
    prefix : string, default="DJANGO_ENV_"
        Prefix for environment variables.  This prefix will be
        prepended to all variable names before searching for them in
        the environment.
    kwargs : dict, optional
        Dictionary with configuration variables as keys and default
        values as values.

    Returns
    -------
    dict
        A dictionary of configuration variables and their values.
    """
    return merge(kwargs, load_file(fn), load_environment(prefix))


def merge(defaults, file, env):
    """Merge configuration from defaults, file, and environment."""
    config = defaults

    # Merge in file options, if they exist in the defaults.
    for (k, v) in file.items():
        if k in config:
            config[k] = v

    # Merge in environment options, if they exist in the defaults.
    for (k, v) in env.items():
        if k in config:
            config[k] = v

    return config


def load_file(fn, raise_bad_format=True):
    """Attempt to load configuration variables from ``fn``.

    Attempt to load configuration variables from ``fn``.  If ``fn``
    does not exist or is not a recognized format, return an empty
    dict.  Raises ``ImproperlyConfigured`` if the file exists and does
    not match a recognized format unless ``raise_bad_format`` is
    ``False``.

    Parameters
    ----------
    fn : string
        Filename from which to load configuration values.
    raise_bad_format : boolean, default=True
        Determine whether to raise
        ``django.core.exceptions.ImproperlyConfigured`` if the file
        format is not recognized.  Default is ``True``.

    Returns
    -------
    dict
        A dictionary, possibly empty, of configuration variables and
        values.

    Raises
    ------
    django.core.exceptions.ImproperlyConfigured
        Raises an ``ImproperlyConfigured`` exception if the file
        format is not recognized and ``raise_bad_format`` is ``True``.
    """
    # Determine if the file actually exists, and bail if not.
    secrets = {}
    if not Path(fn).is_file():
        warnings.warn(f'File "{fn}" does not exist.')
        return secrets

    # Attempt to load TOML, since python.
    with open(fn, "r") as f:
        try:
            secrets = toml.load(f)
            return secrets
        except (toml.TomlDecodeError) as error:
            print(f"toml error: {error}")
    # Attempt to load JSON.
    with open(fn, "r") as f:
        try:
            secrets = json.load(f)
            return secrets
        except (json.JSONDecodeError) as error:
            print(f"json error: {error}")
            pass
    # Attempt to load YAML, with ruamel.yaml and YAML 1.2.
    # Overachiever.
    with open(fn, "r") as f:
        try:
            yaml = YAML(typ="safe")
            secrets = yaml.load(f)
            return secrets
        except (YAMLError) as error:
            print(f"yaml error: {error}")
            pass
    # Attempt to load BespON.  Geek.
    with open(fn, "r") as f:
        try:
            secrets = bespon.load(f)
            return secrets
        except (bespon.erring.DecodingException) as error:
            print(f"bespon error: {error}")
            pass

    if raise_bad_format:
        raise ImproperlyConfigured(
            f"Configuration file {Path(fn).resolve()} is not a recognized format."
        )

    return secrets


def _keys_are_indices(d):
    """Determine if the keys of a dict are list indices."""
    # All integers?
    keys = []
    for k in d.keys():
        try:
            keys.append(int(k))
        except (ValueError):
            return False

    keys = sorted(keys)

    # Zero start?
    if min(keys) != 0:
        return False

    # Consecutive?
    if keys != list(range(0, max(keys) + 1)):
        return False

    return True


def _convert_dict_to_list(d):
    """Convert a list-style dict to a list."""
    keys = sorted(d.keys())
    the_list = []
    for k in keys:
        the_list.append(d[k])

    return the_list


def _convert_listdict_to_list(ds):
    """Convert lists as dicts to lists in a data structure."""
    for (k, v) in ds.items():
        if isinstance(ds[k], dict):
            # If the item points a dict, descend.
            ds[k] = _convert_listdict_to_list(ds[k])
            # We're back.  Now check if the dict is a list-style dict
            # and maybe convert to a list.
            if _keys_are_indices(ds[k]):
                ds[k] = _convert_dict_to_list(ds[k])

    return ds


def load_environment(prefix="DJANGO_ENV_"):
    """Load Django configuration variables from the enviroment.

    This function searches the environment for variables prepended
    with ``prefix``.  Currently, this function only reliably works for
    string variables, but hopefully will work for other types,
    dictionaries, and lists in the future.

    Parameters
    ----------
    prefix : string, default="DJANGO_ENV_"
        Prefix for environment variables.  This prefix should be
        prepended to all valid variable names in the environment.

    Returns
    -------
    dict
        A dictionary, possibly empty, of configuration variables and
        values.
    """
    config = {}

    for (key, value) in os.environ.items():
        if key.startswith(prefix):
            # Find the prefixed values and strip the prefix.
            if sys.version_info >= (3, 6) and sys.version_info < (3, 9):
                name = key[len(prefix) :]
            else:
                name = key.removeprefix(prefix)

            if "__" not in name:
                # Find the non-dict and non-list pairs and add them to
                # the dict.
                config[name] = value
            else:
                # Handle the flattened data structures, treating the
                # list type variables as dicts.
                # Based on:
                # https://gist.github.com/fmder/494aaa2dd6f8c428cede
                keys = name.split("__")
                sub_config = config
                for k in keys[:-1]:
                    try:
                        if not isinstance(sub_config[k], dict):
                            raise ImproperlyConfigured(
                                f"{k} is defined multiple times in the environment."
                            )
                        sub_config = sub_config[k]
                    except (KeyError):
                        sub_config[k] = {}
                        sub_config = sub_config[k]
                sub_config[keys[-1]] = value

    config = _convert_listdict_to_list(config)

    return config


def dump_environment(config, prefix="DJANGO_ENV_", export=True):
    """Dump configuration as an environment variable string.

    Parameters
    ----------
    config : dict
        The configuration dict.
    prefix : string, default="DJANGO_ENV_"
        Prefix for environment variables.  This prefix should be
        prepended to all valid variable names in the environment.
    export : boolean, default=True
        Prepend each environment variable string with "export ", or
        not.

    Returns
    -------
    string
        The current configuration as a string setting environment
        variables.
    """
    stack = []
    dumps = []
    if export:
        exp = "export "
    else:
        exp = ""

    # Convert the config dict into a list (stack).
    for (k, v) in config.items():
        stack.append((k, v))

    while stack:
        (k, v) = stack.pop(0)
        if isinstance(v, list):
            for (i, sv) in enumerate(v):
                stack.append((f"{k}_{i}", sv))
        elif isinstance(v, dict):
            for (sk, sv) in v.items():
                stack.append((f"{k}_{sk}", sv))
        else:
            dumps.append(f"{str(k)}='{str(v)}'")

    return "\n".join(f"{exp}{prefix}{line}" for line in dumps)


def validate_not_empty_string(name, val):
    """Validate that ``val`` is not an empty string.

    Validate that ``val`` is not an empty string.

    Parameters
    ----------
    val : any
        Configuration variable to validate.

    Returns
    -------
    boolean
        ``True`` if ``val`` is not an empty string.

    Raises
    ------
    django.core.exceptions.ImproperlyConfigured
        Raises an ``ImproperlyConfigured`` exception on empty strings,
        with an error message.
    """
    if val == "":
        raise ImproperlyConfigured(f"{name} is an empty string and should not be")

    return True


def validate_falsy(name, val):
    """Validate that ``val`` is falsy.

    Validate that ``val`` is falsy according to
    https://docs.python.org/3/library/stdtypes.html#truth-value-testing.

    Parameters
    ----------
    val : any
        Configuration variable to validate.

    Returns
    -------
    boolean
        ``True`` if ``val`` is falsy.

    Raises
    ------
    django.core.exceptions.ImproperlyConfigured
        Raises an ``ImproperlyConfigured`` exception on truthy values,
        with an error message.
    """
    if val:
        raise ImproperlyConfigured(
            f"{name} has value {val} which is truthy, but should be falsy"
        )

    return True


def validate_truthy(name, val):
    """Validate that ``val`` is truthy.

    Validate that ``val`` is truthy according to
    https://docs.python.org/3/library/stdtypes.html#truth-value-testing.

    Parameters
    ----------
    val : any
        Configuration variable to validate.

    Returns
    -------
    boolean
        ``True`` if ``val`` is truthy.

    Raises
    ------
    django.core.exceptions.ImproperlyConfigured
        Raises an ``ImproperlyConfigured`` exception on falsy values,
        with an error message.
    """
    if not val:
        raise ImproperlyConfigured(
            f"{name} has value {val} which is falsy, but should be truthy"
        )

    return True


# def set_or_fail_on_unset(val):
#     """Raise ``ImproperlyConfigured()`` if ``val`` is not set.

#     Return the configuration value if set, otherwise raise
#     ``django.core.exceptions.ImproperlyConfigured()`` to abort.

#     Parameters
#     ----------
#     val : string
#         Configuration variable that should be set to a value.

#     Returns
#     -------
#     string
#         The variable value, if set.
#     """
#     if not val:
#         raise ImproperlyConfigured("A required configuration variable is not set.")

#     return val


# def _validate(name, val, validation=[]):
#     """Validate a django configuration variable."""
#     env_name = "DJANGO_" + name

#     if isinstance(validation, types.FunctionType):
#         try:
#             return validation(val)
#         except ImproperlyConfigured:
#             raise
#     else:
#         if len(validation) > 0:
#             if not (val in validation):
#                 raise ImproperlyConfigured(
#                     f"{name} can not have value {val};"
#                     f" must be one of [{', '.join(validation)}]."
#                 )
#                 return

#         print(f"{name} loaded from {env_name}.")
#         return val


def dump_secrets(fmt="TOML", **kwargs):
    """Dump a secrets dictionary to the specified format.

    Dump a secrets dictionary to the specified format, defaulting to
    TOML.

    Parameters
    ----------
    fmt : string, default="TOML"
        The dump format, one of ``TOML``, ``JSON``, ``YAML``,
        ``BespON``, or ``ENV``.
    kwargs : dict
        A dictionary of configuration variables.
    """
    if fmt == "TOML":
        return toml.dumps(kwargs)
    elif fmt == "JSON":
        return json.dumps(kwargs)
    elif fmt == "YAML":
        # Let's jump through some hoops for the sake of streams.
        # https://yaml.readthedocs.io/en/latest/example.html#output-of-dump-as-a-string
        from ruamel.yaml.compat import StringIO

        stream = StringIO()
        yaml = YAML(typ="safe")
        yaml.dump(kwargs, stream)
        return stream.getvalue()
    elif fmt == "BespON":
        return bespon.dumps(kwargs)
    else:
        return dump_environment(kwargs)


def main():
    """Run as script, to access ``dump()`` functions."""
    # Desired functions:
    # create SECRET_KEY
    # load and dump environment
    # cli help
    # cli copyright/license
    print(dump_secrets(**load_secrets(**{"ALLOWED_HOSTS": ["bob is your uncle"]})))


if __name__ == "__main__":
    main()
