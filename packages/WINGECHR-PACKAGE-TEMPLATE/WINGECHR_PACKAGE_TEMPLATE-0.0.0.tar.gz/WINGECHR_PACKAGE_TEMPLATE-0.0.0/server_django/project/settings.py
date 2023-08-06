# coding: utf-8

import logging
import os
import sys
from urllib.parse import urljoin

from _local.settings import *  # noqa: F403

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "main.apps.AppConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

ROOT_URLCONF = "project.urls"
WSGI_APPLICATION = "project.wsgi.application"

if "test" in sys.argv:
    DATABASES = {"default": TEST_DATABASE}  # noqa: F405
else:
    DATABASES = {"default": DEFAULT_DATABASE}  # noqa: F405

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = urljoin(BASE_URL, "static/")  # noqa: F405
STATIC_ROOT = os.path.join(BASE_DIR, "_static/")

MEDIA_URL = urljoin(BASE_URL, "media/")  # noqa: F405
MEDIA_ROOT = os.path.join(BASE_DIR, "_local/media/")

AUTH_PASSWORD_VALIDATORS = []

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

LOGLEVEL = logging.INFO if DEBUG else logging.WARNING  # noqa: F405
logger = logging.getLogger()
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s %(funcName)s] %(message)s")
fileHandler = logging.FileHandler(os.path.join(BASE_DIR, "_local", "log.txt"))
fileHandler.setFormatter(logFormatter)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.setLevel(LOGLEVEL)
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

IMAGE = {
    "SIZE": 1024,
    "EXTENSION": "jpg",
    "QUALITY": 75,
    "TMP_DIR": "image_tmp",
    "DIR": "img",
}

DOWNLOAD_XLSX_FILENAME = "Projekte.xlsx"
