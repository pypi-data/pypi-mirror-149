# ******************************************************************************
#
# django-loader, a configuration and secret loader for Django
#
# fake/wsgi.py:  fake project WSGI configuration
#
# Copyright (C) 2021 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************
#
"""Fake project WSGI configuration.

It exposes the WSGI callable as a module-level variable named
``application``.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fake.settings")

application = get_wsgi_application()
