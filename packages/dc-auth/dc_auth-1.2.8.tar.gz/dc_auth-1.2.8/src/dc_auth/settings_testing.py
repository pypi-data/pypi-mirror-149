# flake8: noqa
# pylint: skip-file
import os
from .settings import *

DEBUG = True

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "dc_auth_testing",
    }
}


INSTALLED_APPS = [
    # -- dc apps
    "dc_auth",
    "django_cas_ng",
    # -- modules and frameworks
    "cookielaw",
    "django_extensions",
    # -- core django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

ROOT_URLCONF = "dc_auth.urls"
STATIC_URL = "/static/"

# Json serializer was having a hard time
SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"

CAS_SERVER_URL = DEVELOPMENT_CAS_SERVER_URL
# No need to test the message framework
CAS_LOGIN_MSG = None
AUTHENTICATION_BACKENDS = ["django_cas_ng.backends.CASBackend"]
MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django_cas_ng.middleware.CASMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django_settings_export.settings_export",
            ],
        },
    },
]


# ---------------------- Internationalization ----------------------

LANGUAGE_CODE = "en-au"
TIME_ZONE = "Australia/Sydney"
USE_I18N = True
USE_L10N = True
USE_TZ = True
