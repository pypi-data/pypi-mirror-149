# coding: utf-8
import os

LOCAL_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# e.g. /url/, corresponding to apache.conf: WSGIScriptAlias /url /path/to/wsgi.py
BASE_URL = "/"
SITE_TITLE = "TITLE"
LANGUAGE_CODE = "en-US"
TIME_ZONE = "Europe/Berlin"
DEBUG = True
SECRET_KEY = "**********************************"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "my.domain.com"]
ALLOW_BROWSER_API = True
ALLOW_ADMIN = True

DBNAME = SITE_TITLE.lower().replace(" ", "")

MYSQL_DATABASE = {
    "ENGINE": "django.db.backends.mysql",
    "NAME": DBNAME,
    "USER": DBNAME,
    "PASSWORD": "xxxxxxxxxxxxxxxxxxxxxx",
    "OPTIONS": {"sql_mode": "traditional"},
}

# MYSQL:
# create database DBNAME;
# grant all privileges on DBNAME.* to DBNAME@localhost identified by 'PASSWORD'
# flush privileges;

SQLITE_DATABASE = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": os.path.join(LOCAL_BASE_DIR, "db.sqlite3"),
}

TEST_DATABASE = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": os.path.join(LOCAL_BASE_DIR, "test_db.sqlite3"),
}

DEFAULT_DATABASE = SQLITE_DATABASE
