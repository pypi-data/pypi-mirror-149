# coding: utf-8
import logging  # noqa

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url=settings.BASE_URL + "accounts/login/")
def index(request):
    context = {"LANGUAGE_CODE": settings.LANGUAGE_CODE}
    return render(request, "main/index.html", context)
