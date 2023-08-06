# ******************************************************************************
#
# django-loader, a configuration and secret loader for Django
#
# Copyright 2021-2022 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************
#
"""Fake project settings."""

from pathlib import Path

from django import VERSION

import loader

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-1=-fer_+5!(w&hp_a2++9cl+q@k45y#)xtdnt0x-7xri*-gs0$"
DEBUG = True

secrets = loader.load_secrets(
    **{
        "ALLOWED_HOSTS": [],
    }
)

ALLOWED_HOSTS = secrets["ALLOWED_HOSTS"]

# Application definition.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "fake.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "fake.wsgi.application"

# Database.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation.
VALIDATORS = [
    "UserAttributeSimilarityValidator",
    "MinimumLengthValidator",
    "CommonPasswordValidator",
    "NumericPasswordValidator",
]

AUTH_PASSWORD_VALIDATORS = []

for validator in VALIDATORS:
    prefix = "django.contrib.auth.password_validation."
    AUTH_PASSWORD_VALIDATORS.append({"NAME": prefix + validator})

# Internationalization.
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

if VERSION < (4, 0, 0):
    USE_L10N = True

# Static files.
STATIC_URL = "/static/"

# Default primary key field.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
