# coding: utf-8
from django.urls import include, path  # noqa

from .views import index

urlpatterns = [path("", index, name="index")]
