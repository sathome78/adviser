"""
Django settings for exrates_adviser project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from gettext import gettext

from clients.utils import get_config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', '%9t2&1x41@436xk!h=*dhkt746mjl&jhl#tda@+d^44_@_8_#&')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', True)


ALLOWED_HOSTS = ['localhost', '127.0.0.1', '172.10.10.71']

# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'adviser',

    ]

LANGUAGES = (
    ('ru', gettext('Russian')),
    ('en', gettext('English')),
    )
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = ('en', 'ru')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

ROOT_URLCONF = 'exrates_adviser.urls'

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
                ],
            },
        },
    ]

#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, 'static')
#]


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'testdjangoapp1@gmail.com'
EMAIL_HOST_PASSWORD = 'passtest0'

config = get_config()
PIPEDRIVE_URL = config.get('DEFAULT', 'PIPEDRIVE_URL')
CLIENT_SECRET = config.get('DEFAULT', 'CLIENT_SECRET')

ZENDESK_URL = config.get('DEFAULT', 'ZENDESK_URL')
ZENDESK_TOKEN = config.get('DEFAULT', 'ZENDESK_TOKEN')
ZENDESK_EMAIL = config.get('DEFAULT', 'ZENDESK_EMAIL')

USER_TELEGRAM = config.get('PIPEDRIVE_FIELDS', 'user_telegram')
ORG_LINK_TO_PROJECT = config.get('PIPEDRIVE_FIELDS', 'org_link_to_project')
USER_LINKEDIN = config.get('PIPEDRIVE_FIELDS', 'user_linked_in')

USER_LINK_TO_FORM = config.get('PIPEDRIVE_FIELDS', 'user_link_to_form')
USER_LINK_TO_DETAILS = config.get('PIPEDRIVE_FIELDS', 'user_link_to_details')

DOMAIN = config.get('DEFAULT', 'DOMAIN')

PIPELINE_CHANNELS = {
    "IEO": 2,
    "Listing": 3
    }

WSGI_APPLICATION = 'exrates_adviser.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.getenv('SQLITE_FILE_PATH', os.path.join(BASE_DIR, 'db.sqlite3')),
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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.getenv('STATIC_ROOT_DIRECROTY', os.path.join(BASE_DIR, 'static'))
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

