# Django settings for box project.

import os
import sys

ABS_PATH = os.path.dirname(os.path.abspath(__file__))

APP_BASEDIR = os.path.dirname(ABS_PATH)
APP_MODULE = ABS_PATH.split('/')[-1]

DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'root@oekohosting.ch'
DATE_FORMAT = 'd.m.Y'

DEBUG = 'runserver' in sys.argv
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('FEINHEIT Developers', 'dev@feinheit.ch'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'data.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'Europe/Zurich'
LANGUAGE_CODE = 'de-ch'

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(APP_BASEDIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(APP_BASEDIR, 'static')
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
    'box.debug.DebugFooter',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'box.middleware.ForceDomainMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',

    'django.contrib.auth.context_processors.auth',

    'feincms.context_processors.add_page_if_missing',
    'box.context_processors.box',

    'django.contrib.messages.context_processors.messages',
)

ROOT_URLCONF = 'box.urls'

TEMPLATE_DIRS = (
    os.path.join(APP_BASEDIR, APP_MODULE, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'django.contrib.staticfiles',

    'box',
    'box.cms',

    'towel_foundation',
    'towel',

    'feincms',
    'feincms.module.medialibrary',
    'feincms.module.page',
    'mptt',
    'form_designer',
    'elephantblog',

    'south',
    'compressor',

    'django.contrib.admin',
)

LANGUAGES = (
    #('en', 'English'),
    ('de', 'German'),
    #('fr', 'French'),
    #('it', 'Italian'),
)

SOUTH_MIGRATION_MODULES = dict((app, 'box.migrate.%s' % app) for app in (
    'page',
    'medialibrary',
    'elephantblog',
))

FEINCMS_ADMIN_MEDIA = '/static/feincms/'
TINYMCE_JS_URL = '/static/tinymce/tiny_mce.js'

FEINCMS_RICHTEXT_INIT_TEMPLATE = 'admin/content/richtext/init_ckeditor.html'
FEINCMS_RICHTEXT_INIT_CONTEXT = {
    'CKEDITOR_JS_URL': '/static/ckeditor/ckeditor.js',
}


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

LOCALE_PATHS = (
    os.path.join(APP_BASEDIR, 'conf', 'locale'),
)

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local_settings import *  # noqa
except ImportError:
    pass
