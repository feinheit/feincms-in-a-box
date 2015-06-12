# Django settings for box project.

from __future__ import absolute_import, unicode_literals

from env import env
import dj_database_url
import django_cache_url
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False
TESTING = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('FEINHEIT Developers', 'dev@feinheit.ch'),
)
MANAGERS = ADMINS
DEFAULT_FROM_EMAIL = 'no-reply@${DOMAIN}'
SERVER_EMAIL = 'root@oekohosting.ch'

DATABASES = {
    'default': dj_database_url.config(),
}

CACHES = {
    'default': django_cache_url.config(),
}

SECRET_KEY = env('SECRET_KEY', required=True)
FORCE_DOMAIN = env('FORCE_DOMAIN')
ALLOWED_HOSTS = env('ALLOWED_HOSTS', required=True)

TIME_ZONE = 'Europe/Zurich'
LANGUAGE_CODE = 'de-ch'
LANGUAGES = (
    # ('en', 'English'),
    ('de', 'German'),
    # ('fr', 'French'),
    # ('it', 'Italian'),
)

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MIDDLEWARE_CLASSES = (
    '${PROJECT_NAME}.middleware.ForceDomainMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    '${PROJECT_NAME}.middleware.OnlyStaffMiddleware',
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
    '${PROJECT_NAME}.context_processors.site_context',
)

ROOT_URLCONF = '${PROJECT_NAME}.urls'
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, '${PROJECT_NAME}', 'templates'),
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

    '${PROJECT_NAME}',
    '${PROJECT_NAME}.cms',

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

    'flat',
    'django.contrib.admin',
    'admin_sso',
)

MIGRATION_MODULES = dict((app, '${PROJECT_NAME}.migrate.%s' % app) for app in (
    'page',
    'medialibrary',
    'elephantblog',
))

FEINCMS_RICHTEXT_INIT_TEMPLATE = 'admin/content/richtext/init_ckeditor.html'
FEINCMS_RICHTEXT_INIT_CONTEXT = {
    'CKEDITOR_JS_URL': '//cdn.ckeditor.com/4.4.5.1/standard/ckeditor.js',
}

DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID = env(
    'DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID')
DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET = env(
    'DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET')
DJANGO_ADMIN_SSO_ADD_LOGIN_BUTTON = all((
    DJANGO_ADMIN_SSO_OAUTH_CLIENT_ID,
    DJANGO_ADMIN_SSO_OAUTH_CLIENT_SECRET,
))
DJANGO_ADMIN_SSO_AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
DJANGO_ADMIN_SSO_TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
DJANGO_ADMIN_SSO_REVOKE_URI = 'https://accounts.google.com/o/oauth2/revoke'
AUTHENTICATION_BACKENDS = (
    'admin_sso.auth.DjangoSSOAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True


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

BLOG_TITLE = '${NICE_NAME}'
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
            '()': '${PROJECT_NAME}.tools.logging.SkipUnreadablePostError',
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
                'skip_unreadable_post_error',
            ],
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log', 'info.log'),
            'formatter': 'verbose',
            'maxBytes': 500000,  # 500 kB
            'backupCount': 4
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

RAVEN_CONFIG = {
    'dsn': env('SENTRY_DSN'),
}
