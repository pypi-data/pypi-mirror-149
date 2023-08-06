# ******************************************************************************
#
# django-loader, a configuration and secret loader for Django
#
# fake/urls.py:  fake project URL routing
#
# Copyright (C) 2021 Jeremy A Gray <gray@flyquackswim.com>.
#
# SPDX-License-Identifier: MIT
#
# ******************************************************************************

"""Fake project URL routing."""

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]
