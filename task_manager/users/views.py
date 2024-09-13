from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation.trans_real import gettext as _
from django.views.generic import (
    FormView,
    TemplateView,
)

from task_manager.users.form import RegisterUserForm
from task_manager.users.user_service import UserService
from task_manager.users.utils import (
    CreateUserFormMixin,
    DeleteUserMixin,
    UpdateUserFormMixin,
)


class UsersListView(TemplateView):
    template_name = 'users/users_list.html'
    extra_context = {
        'object_list': UserService().get_all_users(),
    }


class RegisterUserView(CreateUserFormMixin, FormView):
    template_name = 'users/user_create_form.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')
    success_message = _('You have been registered successfully.')

    title_form = _('Registration')
    name_button_in_form = _('Register')

    def form_valid(self, form: RegisterUserForm) -> HttpResponse:
        return self.mixin_form_valid(form)


class UserUpdateView(UpdateUserFormMixin, FormView):
    form_class = RegisterUserForm
    template_name = 'users/user_update_form.html'
    success_url = reverse_lazy('users_list')

    title_form = _('Edit user')
    name_button_in_form = _('Update')
    service = UserService()

    def form_valid(self, form: RegisterUserForm) -> HttpResponse:
        return self.mixin_form_valid(form, is_update=True)


class UserDeleteView(DeleteUserMixin, TemplateView):
    success_message = _('User successfully deleted.')
    template_name = "users/user_delete.html"

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return self.delete(request)


class LoginInView(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_message = _('You have been logged in.')


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.info(request, _('You have been logged out.'))
    return redirect(reverse_lazy('index'))
