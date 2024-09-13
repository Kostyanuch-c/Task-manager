from django.contrib import messages
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.users.entities import UserCreate
from task_manager.users.exceptions import (
    ServiceNotDefinedError,
    UsernameIsNotFreeError,
)
from task_manager.users.user_service import UserService


class DataFormMixin:
    """Adds access to the filled attributes to the template"""
    title_form = None
    name_button_in_form = None
    extra_context = {}

    def __init__(self):
        if self.title_form is not None:
            self.extra_context['title_form'] = self.title_form
        if self.name_button_in_form is not None:
            self.extra_context['name_button_in_form'] = self.name_button_in_form


class PermissionsUserChangeMixin:
    """
    Overrides the dispatch method.
    First of all it checks whether the user is authorized.
    And then his rights to change, also adds flash messages
    """
    message_failed_authenticated = _('You are not authorized! Please log in.')
    message_failed_permissions = _(
        "You do not have permission to change another user.",
    )
    redirect_authenticated = reverse_lazy('login')
    redirect_failed_permissions = reverse_lazy('users_list')
    service = None

    def get_object(self):
        if self.service is None:
            raise ServiceNotDefinedError(_('Service not defined'))
        user_id = self.kwargs.get('pk', 0)
        user = self.service.get_object(user_id)
        return user

    def has_permission(self) -> bool:
        """ Check if the current user is the object owner """
        return self.get_object() == self.request.user.to_entity()

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.user.is_authenticated:
            messages.error(request, self.message_failed_authenticated)
            return redirect(self.redirect_authenticated)
        if not self.has_permission():
            messages.error(request, self.message_failed_permissions)
            return redirect(self.redirect_failed_permissions)
        return super().dispatch(request, *args, **kwargs)


class CreateUserFormMixin(DataFormMixin):
    """ Mixin to handle the logic for creating or updating users. """
    success_message = _('User created successfully')
    success_message_update = _('User successfully changed.')

    def mixin_form_valid(self, form, is_update=False) -> HttpResponse:
        user_service = UserService()
        user_data = UserCreate(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
        )
        try:
            if is_update:
                user_service.update_user(user_data)
                messages.success(self.request, self.success_message_update)
            else:
                user_service.register_user(user_data)
                messages.success(self.request, self.success_message)
            return super().form_valid(form)

        except UsernameIsNotFreeError:
            form.add_error('username', _('Username is already taken.'))
            return self.form_invalid(form)


class UpdateUserFormMixin(
    CreateUserFormMixin,
    PermissionsUserChangeMixin,
    DataFormMixin,
):
    """ Mixin for handling user update"""


class DeleteUserMixin(PermissionsUserChangeMixin):
    """ Mixin for handling user deletion """
    success_message = _('User successfully deleted.')

    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user_service = UserService()
        user_id = self.kwargs.get('pk', 0)

        user_service.delete_user(user_id)
        messages.success(request, self.success_message)
        return redirect(self.redirect_failed_permissions)
