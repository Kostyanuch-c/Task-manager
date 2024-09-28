from http import HTTPStatus

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import (
    redirect,
    render,
)
from django.urls import reverse_lazy
from django.utils.translation.trans_real import gettext as _
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


class LoginInView(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = "users/login.html"
    success_message = _("You have been logged in.")


def logout_view(request):
    logout(request)
    messages.info(request, _("You have been logged out."))
    return redirect(reverse_lazy("index"))


def page_not_found_view(request, exception):
    return render(request, "errors/404.html", status=HTTPStatus.NOT_FOUND)
