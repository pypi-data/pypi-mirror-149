===============
 django-loader
===============

django-loader: a configuration variable and secrets loader for Django
apps.

.. image:: https://badge.fury.io/py/django-loader.svg
   :target: https://badge.fury.io/py/django-loader
   :alt: PyPI Version
.. image:: https://readthedocs.org/projects/django-loader/badge/?version=latest
   :target: https://django-loader.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

What is django-loader?
======================

django-loader is a configuration variable and secrets loader for
Django apps.  It loads a dictionary of configuration variables into
``settings.py`` that consists of default values, values from a
configuration file (like ``.env``) and from environment variables.  It
can load configuration files in TOML, JSON, YAML, and BespON formats.
The script interface is able to convert between all available formats.

Roadmap
=======

#. Change from loading one configuration file to one or a list of
   configuration files, with successive files having precedence over
   previous ones.
#. Implement validation functions to provide for customizable data
   validation and security checks.
#. Add simple command line interface options with ``argparse`` and add
   usage to doumentation.

Installation
============

Install django-loader with::

  pip install django-loader
  pip freeze > requirements.txt

or add as a poetry dependency.

If you desire a package locally built with poetry, download the
source, change the appropriate lines in ``pyproject.toml``, and
rebuild.

Usage
=====

Console::

  loader file format

In Python::

  >>> import loader
  >>> secrets = loader.load_secrets(**{"SECRET_KEY": ""})
  >>> SECRET_KEY = secrets["SECRET_KEY"]

See the source and `documentation
<https://django-loader.readthedocs.io/en/latest/>`_ for more
information.

Configuration
=============

There are no configuration files or options; all configurable options
will be accessible as function parameters or options in the command
line interface.

Copyright and License
=====================

SPDX-License-Identifier: `MIT <https://spdx.org/licenses/MTI.html>`_

django-loader:  a configuration variable and secrets loader for Django
apps.

Copyright (C) 2021 `Jeremy A Gray <gray@flyquackswim.com>`_.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Author
======

`Jeremy A Gray <gray@flyquackswim.com>`_
