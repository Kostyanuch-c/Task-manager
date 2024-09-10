from django.contrib.auth import logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation.trans_real import gettext as _
from django.views.generic import CreateView, ListView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.users.form import RegisterUserForm


class LoginInView(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_message = _('You have been logged in.')


def logout_view(request):
    logout(request)
    messages.info(request, _('You have been logged out.'))
    return redirect(reverse_lazy('index'))


class RegisterUserView(SuccessMessageMixin, CreateView):
    model = get_user_model()
    form_class = RegisterUserForm
    template_name = 'users/user_create_form.html'
    success_url = reverse_lazy('login')
    success_message = _('You have been registered successfully.')


class GetUsersView(ListView):
    model = get_user_model()
    template_name = 'users/users_list.html'
