from http import HTTPStatus

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.utils.translation.trans_real import gettext as _
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


class LoginInView(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = "users/login.html"
    success_message = _("You have been logged in.")


class LogoutsView(LogoutView):
    success_message = _("You have been logged out.")

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().dispatch(request, *args, **kwargs)


class ErrorView:
    @staticmethod
    def page_not_found(request, exception):
        return render(request, "errors/404.html", status=HTTPStatus.NOT_FOUND)
