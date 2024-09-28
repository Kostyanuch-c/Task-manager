from http import HTTPStatus

from django.contrib.auth import logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation.trans_real import gettext as _
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.users.form import RegisterUserForm


class IndexView(TemplateView):
    template_name = "index.html"


class LoginInView(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_message = _('You have been logged in.')


def logout_view(request):
    logout(request)
    messages.info(request, _('You have been logged out.'))
    return redirect(reverse_lazy('index'))


def page_not_found_view(request, exception):
    return render(request, "errors/404.html", status=HTTPStatus.NOT_FOUND)
