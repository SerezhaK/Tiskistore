"""
Django settings for Tiskistore project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

# import os
from pathlib import Path

from environ import Env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = Env(DEBUG=(bool, False))

Env.read_env(str(BASE_DIR / ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

DOCKER = env('DOCKER', default=False)

PHONE_NUMBER_CONFIRM = env.bool('PHONE_NUMBER_CONFIRM')

DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# noinspection PyUnresolvedReferences
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'drf_spectacular',
    'products',
    'users',
    'order',
    "phonenumber_field",
    "cart",
    "smsru",

]

# noinspection PyUnresolvedReferences
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Tiskistore.urls"

# noinspection PyUnresolvedReferences
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Tiskistore.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
            "django.contrib.auth" +
            ".password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME":
            "django.contrib.auth" +
            ".password_validation.MinimumLengthValidator",
    },
    {
        "NAME":
            "django.contrib.auth" +
            ".password_validation.CommonPasswordValidator",
    },
    {
        "NAME":
            "django.contrib.auth" +
            ".password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = 'static'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = 'media'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1', ]

AUTH_USER_MODEL = 'users.User'

# ADMIN_MEDIA_PREFIX = '/admin/media/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'EXCEPTION_HANDLER': 'core.exceptions.custom_exception_handler',
}

FIXTURE_DIRS = [
    'fixtures',
]

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
    }
}
# Configure the phone_number_field (for django-phonenumber-field integration)
# Check https://django-phonenumber-field.readthedocs.io/en/latest/reference.html#std-setting-PHONENUMBER_DEFAULT_REGION
PHONENUMBER_DB_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_REGION = "RU"

# Configure the SENDSMS_BACKEND (for django-smsru integration)
# Check https://github.com/iredun/django-smsru
if PHONE_NUMBER_CONFIRM:
    TISKI_STORE_CONFIRM_KEY = 'user_confirm_{token}'
    TISKI_STORE_RESET_CODE = 'password_reset_{token}'
    TISKI_STORE_USER_CONFIRM_TIMEOUT = 300
    SMS_RU = {
        # Either password and login or api_id must be specified
        "API_ID": env.str('API_ID'),
        "LOGIN": env.str('LOGIN'),
        "PASSWORD": env.str('PASSWORD'),
        "TEST": True,  # Sending in test mode defaults to False
        "SENDER": 'sms',
        "PARTNER_ID": 1111
    }
