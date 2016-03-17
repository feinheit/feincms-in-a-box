# coding: utf-8
"""
Entry point for local development.
"""
from __future__ import absolute_import, unicode_literals
from .common import *  # noqa

DEBUG = True
TEMPLATE_DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
LOGGING['loggers'].update({
    # Uncomment to dump SQL statements.
    # 'django.db.backends': {
    #     'level': 'DEBUG',
    #     'handlers': ['console'],
    #     'propagate': False,
    # },
    'django.request': {
        'level': 'DEBUG',
        'handlers': ['console'],  # Dump exceptions to the console.
        'propagate': False,
    },
    '${PROJECT_NAME}': {
        'level': 'DEBUG',
        'handlers': ['console'],  # Dump app logs to the console.
        'propagate': False,
    },
})

INSTALLED_APPS += (
    'debug_toolbar.apps.DebugToolbarConfig',
)
INTERNAL_IPS = ('127.0.0.1',)
MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
) + MIDDLEWARE_CLASSES
DEBUG_TOOLBAR_PATCH_SETTINGS = False

THUMBNAIL_DEBUG = True

RAVEN_CONFIG = {'dsn': ''}

WEBPACK_LOADER['DEFAULT'].update({
    'BUNDLE_DIR_NAME': 'build/',
    'STATS_FILE': os.path.join(BASE_DIR, 'tmp', 'webpack-stats.json'),
})

# `debug` is only True in templates if the vistor IP is in INTERNAL_IPS.
INTERNAL_IPS = type('c', (), {'__contains__': lambda *a: True})()
