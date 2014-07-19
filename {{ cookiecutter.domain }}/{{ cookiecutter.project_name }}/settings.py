# Django settings for box project.

from __future__ import absolute_import, unicode_literals

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = any(r in sys.argv for r in ('runserver', 'shell', 'dbshell', 'test'))
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('FEINHEIT Developers', 'dev@feinheit.ch'),
)
MANAGERS = ADMINS
DEFAULT_FROM_EMAIL = 'no-reply@{{ cookiecutter.domain }}'
SERVER_EMAIL = 'root@oekohosting.ch'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'data.db',
    }
}

TIME_ZONE = 'Europe/Zurich'
LANGUAGE_CODE = 'de-ch'

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

if not DEBUG:
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MIDDLEWARE_CLASSES = (
    '{{ cookiecutter.project_name }}.middleware.ForceDomainMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',  # 1.7
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'feincms.context_processors.add_page_if_missing',
    '{{ cookiecutter.project_name }}.context_processors.{{ cookiecutter.project_name }}_context',
)

ROOT_URLCONF = '{{ cookiecutter.project_name }}.urls'
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, '{{ cookiecutter.project_name }}', 'templates'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'conf', 'locale'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    '{{ cookiecutter.project_name }}',
    '{{ cookiecutter.project_name }}.cms',

    'towel_foundation',
    'towel',

    'feincms',
    'feincms.module.medialibrary',
    'feincms.module.page',
    'mptt',
    'form_designer',
    'elephantblog',
    'feincms_oembed',

    'compressor',

    'django.contrib.admin',
    'admin_sso',
)

LANGUAGES = (
    # ('en', 'English'),
    ('de', 'German'),
    # ('fr', 'French'),
    # ('it', 'Italian'),
)

MIGRATION_MODULES = dict((app, '{{ cookiecutter.project_name }}.migrate.%s' % app) for app in (
    'page',
    'medialibrary',
    'elephantblog',
))

FEINCMS_RICHTEXT_INIT_TEMPLATE = 'admin/content/richtext/init_ckeditor.html'
FEINCMS_RICHTEXT_INIT_CONTEXT = {
    'CKEDITOR_JS_URL': '/static/ckeditor/ckeditor.js',
}

DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID = ''
DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET = ''
DJANGO_ADMIN_SSO_AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
DJANGO_ADMIN_SSO_TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
DJANGO_ADMIN_SSO_REVOKE_URI = 'https://accounts.google.com/o/oauth2/revoke'
DJANGO_ADMIN_SSO_ADD_LOGIN_BUTTON = False
AUTHENTICATION_BACKENDS = (
    'admin_sso.auth.DjangoSSOAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)


def elephantblog_entry_url_app(self):
    from feincms.content.application.models import app_reverse
    return app_reverse('elephantblog_entry_detail', 'elephantblog', kwargs={
        'year': self.published_on.strftime('%Y'),
        'month': self.published_on.strftime('%m'),
        'day': self.published_on.strftime('%d'),
        'slug': self.slug,
    })


def elephantblog_category_url_app(self):
    from feincms.content.application.models import app_reverse
    return app_reverse('elephantblog_category_detail', 'elephantblog', kwargs={
        'slug': self.translation.slug,
    })


ABSOLUTE_URL_OVERRIDES = {
    'elephantblog.entry': elephantblog_entry_url_app,
    'elephantblog.category': elephantblog_category_url_app,
}

BLOG_TITLE = 'FeinCMS-in-a-Box'
BLOG_DESCRIPTION = 'News'
BLOG_PAGINATE_BY = 10

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'skip_unreadable_post_error': {
            '()': '{{ cookiecutter.project_name }}.utils.SkipUnreadablePostError',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(message)s',
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
            'filters': [
                'require_debug_false',
                # 'skip_unreadable_post_error',
            ],
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        # Root handler.
        '': {
            'handlers': ['sentry'],
        },
        'django.request': {
            'handlers': ['sentry'],
        },
    },
}

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    LOGGING['loggers'].update({
        'django.db.backends': {
            'level': 'DEBUG',
            # 'handlers': ['console'],  # Uncomment to dump SQL statements.
            'propagate': False,
        },
        'django.request': {
            'level': DEBUG,
            'handlers': ['console'],  # Dump exceptions to the console.
            'propagate': False,
        },
    })
    INSTALLED_APPS += (
        'debug_toolbar',  # Django 1.7: debug_toolbar.apps.DebugToolbarConfig
    )
    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE_CLASSES = (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ) + MIDDLEWARE_CLASSES
    DEBUG_TOOLBAR_PATCH_SETTINGS = False

try:
    from .local_settings import *  # noqa
except ImportError:
    pass
