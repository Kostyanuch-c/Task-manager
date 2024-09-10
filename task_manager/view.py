from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.utils.translation import gettext as _


class IndexView(TemplateView):
    template_name = "index.html"
