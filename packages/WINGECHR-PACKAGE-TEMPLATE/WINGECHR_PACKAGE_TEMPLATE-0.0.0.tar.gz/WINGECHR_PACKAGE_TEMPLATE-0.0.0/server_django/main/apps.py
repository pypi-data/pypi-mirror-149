# coding: utf-8
from django.apps import AppConfig
from django.conf import settings


class AppConfig(AppConfig):
    name = "main"
    verbose_name = settings.SITE_TITLE
