"""
Django settings for exrates_adviser project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
# -*- coding: utf-8 -*-
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from gettext import gettext

from clients.utils import get_config
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', '%9t2&1x41@436xk!h=*dhkt746mjl&jhl#tda@+d^44_@_8_#&')
# SECURITY WARNING: don't run with debug turned on in production!
config = get_config()
DEBUG = config.getboolean('DEFAULT', 'DEBUG')


ALLOWED_HOSTS = ['localhost', '127.0.0.1', '172.10.10.71', '172.31.28.213', 'about.exrates.me', '172.50.100.48', 'coins.exrates.me', 'adviser-devtest.exrates-k8s.name']

# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'rest_framework',
    'adviser',
    'analytics',
    'ckeditor',
    'ckeditor_uploader'

    ]

OPENGRAPH_CONFIG = {
    'FB_ADMINS': '100003930913968',
    'FB_APP_ID': '1335507479837766',
    'SITE_NAME': 'Exrates.me',
}

SITE = config.get('DEFAULT', 'SITE')

LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
    )
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = ('en', 'ru')

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'adviser.context_processor.force_default_language_middleware',
    ]

ROOT_URLCONF = 'exrates_adviser.urls'

CACHE_MIDDLEWARE_ALIAS = 'default'

# Additional prefix for cache keys
CACHE_MIDDLEWARE_KEY_PREFIX = ''

# Cache key TTL in seconds
CACHE_MIDDLEWARE_SECONDS = 600

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "adviser", "templates"),
            os.path.join(BASE_DIR, "templates"),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'adviser.context_processor.from_settings',
                ],
            },
        },
    ]

# STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, 'static')
# ]

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse',
		},
		'require_debug_true': {
			'()': 'django.utils.log.RequireDebugTrue',
		},
	},
	'formatters': {
		'django.server': {
			'()': 'django.utils.log.ServerFormatter',
			'format': '[%(server_time)s] %(message)s',
		}
	},
	'handlers': {
		'console': {
			'level': 'INFO',
			'filters': ['require_debug_true'],
			'class': 'logging.StreamHandler',
		},
		'console_debug_false': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'logging.StreamHandler',
		},
		'django.server': {
			'level': 'INFO',
			'class': 'logging.StreamHandler',
			'formatter': 'django.server',
		},
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler'
		}
	},
	'loggers': {
		'django': {
			'handlers': ['console', 'console_debug_false', 'mail_admins'],
			'level': 'INFO',
		},
		'django.server': {
			'handlers': ['django.server'],
			'level': 'INFO',
			'propagate': False,
		}
	}
}


CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar': 'full',

        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',
            ]},
        ],
'title': True,
       'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
       'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        'height': 291,
        'width': '100%',
        'filebrowserWindowHeight': 725,
        'filebrowserWindowWidth': 940,
        'toolbarCanCollapse': True,
        'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
'mathJaxClass': 'mathjax-latex',
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'image2',
            'mathjax',  # Used to render mathematical formulae
            'codesnippet',  # Used to add code snippets
            'embed',  # Used for embedding media (YouTube/Slideshare etc)
            'tableresize',  # Used to allow resizing of columns in tables

            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}
CKEDITOR_UPLOAD_PATH = 'media/articles'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
        }
    }

config = get_config()


ZENDESK_URL = config.get('DEFAULT', 'ZENDESK_URL')
ZENDESK_TOKEN = config.get('DEFAULT', 'ZENDESK_TOKEN')
ZENDESK_EMAIL = config.get('DEFAULT', 'ZENDESK_EMAIL')


TELEGRAMBOT_TOKEN = config.get('DEFAULT', 'TELEGRAMBOT_TOKEN')
TELEGRAMBOT_CHAT_DEAL = config.get('DEFAULT', 'TELEGRAMBOT_CHAT_DEAL')
TELEGRAMBOT_CHAT_SUPPORT = config.get('DEFAULT', 'TELEGRAMBOT_CHAT_SUPPORT')

DOMAIN = config.get('MYSQL', 'DOMAIN')

MYSQL_USER = config.get('MYSQL', 'MYSQL_USER')
MYSQL_DB_NAME = config.get('MYSQL', 'MYSQL_DB_NAME')
MYSQL_PASSWORD = config.get('MYSQL', 'MYSQL_PASSWORD')

PIPEDRIVE_ME = {"PIPEDRIVE_URL": config.get('DEFAULT', 'PIPEDRIVE_URL'),
                "CLIENT_SECRET": config.get('DEFAULT', 'CLIENT_SECRET'),
                "PIPEDRIVE_NEW_ADVISER": config.get('PIPEDRIVE_FIELDS', 'pipedrive_new_adviser'),
                "PIPEDRIVECHANNEL": config.get('PIPEDRIVE_FIELDS', 'pipedrive_listing'),
                "USER_TELEGRAM": config.get('PIPEDRIVE_FIELDS', 'user_telegram'),
                "USER_LINKEDIN": config.get('PIPEDRIVE_FIELDS', 'user_linked_in'),
                "USER_LINKS": config.get('PIPEDRIVE_FIELDS', 'user_links'),
                "ORG_WEBSITE": config.get('PIPEDRIVE_FIELDS', 'org_website')
                }
PIPEDRIVE = {"PIPEDRIVE_URL": config.get('DEFAULT', 'PIPEDRIVE_URL1'),
                "CLIENT_SECRET": config.get('DEFAULT', 'CLIENT_SECRET1'),
                "PIPEDRIVE_NEW_ADVISER": config.get('PIPEDRIVE_FIELDS1', 'pipedrive_new_adviser'),
                "PIPEDRIVECHANNEL": config.get('PIPEDRIVE_FIELDS1', 'pipedrive_listing'),
                "USER_TELEGRAM": config.get('PIPEDRIVE_FIELDS1', 'user_telegram'),
                "USER_LINKEDIN": config.get('PIPEDRIVE_FIELDS1', 'user_linked_in'),
                "USER_LINKS": config.get('PIPEDRIVE_FIELDS1', 'user_links'),
                "ORG_WEBSITE": config.get('PIPEDRIVE_FIELDS1', 'org_website')
                }

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

WSGI_APPLICATION = 'exrates_adviser.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.getenv('SQLITE_FILE_PATH', os.path.join(BASE_DIR, 'db.sqlite3')),
    #    },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_DB_NAME,
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PASSWORD,
        'HOST': DOMAIN,   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
    }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
    )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# STATIC_ROOT = os.getenv('STATIC_ROOT_DIRECTORY', os.path.join(BASE_DIR, 'static'))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    )
