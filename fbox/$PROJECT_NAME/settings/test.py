# coding: utf-8
""" Entry point for unittests """
from __future__ import absolute_import, unicode_literals
from .common import *  # noqa

# IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3"
    },
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
TESTING = True
LOGGING['loggers'].update({
    # Uncomment to dump SQL statements.
    # 'django.db.backends': {
    #     'level': 'DEBUG',
    #     'handlers': ['console'],
    #     'propagate': False,
    # },
    '': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'django.request': {
        'level': 'ERROR',
        'handlers': ['console'],  # Dump exceptions to the console.
        'propagate': False,
    },
    '${PROJECT_NAME}': {
        'level': 'DEBUG',
        'handlers': ['console'],  # Dump app logs to the console.
        'propagate': False,
    },
})

RAVEN_CONFIG = {'dsn': ''}
