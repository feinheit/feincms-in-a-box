# coding: utf-8
"""
Entry point for the production site.
"""
from __future__ import absolute_import, unicode_literals
from .common import *  # noqa

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
)
