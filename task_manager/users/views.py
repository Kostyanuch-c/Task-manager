from django.contrib.auth import logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation.trans_real import gettext as _
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.users.form import RegisterUserForm
from task_manager.users.utils import DataFormMixin, PermissionsUserChangeMixin


class LoginInView(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_message = _('You have been logged in.')


def logout_view(request):
    logout(request)
    messages.info(request, _('You have been logged out.'))
    return redirect(reverse_lazy('index'))


class RegisterUserView(DataFormMixin, SuccessMessageMixin, CreateView):
    model = get_user_model()
    form_class = RegisterUserForm
    template_name = 'users/user_create_form.html'
    success_url = reverse_lazy('login')
    success_message = _('You have been registered successfully.')

    title_form = _('Registration')
    name_button_in_form = _('Register')


class UsersListView(ListView):
    model = get_user_model()
    template_name = 'users/users_list.html'


class UserUpdateView(PermissionsUserChangeMixin, LoginRequiredMixin,
                     SuccessMessageMixin, DataFormMixin, UpdateView):
    model = get_user_model()
    form_class = RegisterUserForm
    template_name = 'users/user_update_form.html'
    success_url = reverse_lazy('users_list')
    success_message = _('User successfully changed.')

    title_form = _('Edit user')
    name_button_in_form = _('Update')


class UserDeleteView(PermissionsUserChangeMixin, LoginRequiredMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy('users_list')
    success_message = _('User successfully deleted.')
    template_name = "users/user_delete.html"
