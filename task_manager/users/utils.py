from django.contrib import messages
from django.forms import BaseForm
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.users.entities import User as UserEntity
from task_manager.users.exceptions import ServiceNotDefinedError


class BaseServiceMixin:
    """Mixin for init service"""

    service = None

    def __init__(self):
        if self.service is None:
            raise ServiceNotDefinedError


class BaseObjectIdMixin:
    """Mixin for init object id"""

    kwargs_key_for_id = "pk"
    _object_id = None

    def get_object_id(self, **kwargs):
        """Return the object id from urls params"""
        self._object_id = kwargs.get(self.kwargs_key_for_id, 0)
        return self._object_id


class CreateObjectMixin(BaseServiceMixin):
    """Mixin to handle the logic for creating or updating users."""

    success_message = _("Created successfully")

    def mixin_form_valid(
        self,
        request: HttpRequest,
        form: BaseForm,
        object_data,
    ) -> HttpResponse:

        self.service.create_object(object_data)
        messages.success(request, self.success_message)
        return super().form_valid(form)


class PermissionsObjectChangeMixin(BaseObjectIdMixin, BaseServiceMixin):
    """
    Overrides the dispatch method.
    First of all it checks whether the user is authorized.
    And then his rights to change, also adds flash messages
    """

    message_failed_authenticated = _("You are not authorized! Please log in.")
    message_failed_permissions = _(
        "You do not have permission to change another user.",
    )
    redirect_authenticated = reverse_lazy("login")
    redirect_failed_permissions = reverse_lazy("users_list")

    def get_object(self, **kwargs) -> UserEntity:
        """Return object from urls params"""
        owner_object = self.service.get_object(self.get_object_id(**kwargs))
        return owner_object

    def has_permission(self, request: HttpRequest, **kwargs) -> bool:
        """Check if the current user is the object owner"""
        return self.get_object(**kwargs) == request.user.to_entity()

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.user.is_authenticated:
            messages.error(request, self.message_failed_authenticated)
            return redirect(self.redirect_authenticated)

        if not self.has_permission(request=request, **kwargs):
            messages.error(request, self.message_failed_permissions)
            return redirect(self.redirect_failed_permissions)

        return super().dispatch(request, *args, **kwargs)


class UpdateUserFormMixin(PermissionsObjectChangeMixin):
    """Mixin for handling user update"""

    success_message = _("Created successfully")

    def mixin_form_valid(
        self,
        request: HttpRequest,
        form: BaseForm,
        object_data,
    ) -> HttpResponse:
        self.service.update_object(
            user_id=self._object_id,
            user_data=object_data,
        )
        messages.success(request, self.success_message)
        return super().form_valid(form)


class DeleteUserMixin(PermissionsObjectChangeMixin):
    """Mixin for handling user deletion"""

    success_message = _("User successfully deleted.")

    def mixin_context_data(self, context: dict, **kwargs) -> dict:
        context.update(
            {
                "object": self.get_object(**kwargs),
            },
        )
        return context

    def delete(self, request: HttpRequest) -> HttpResponse:
        self.service.delete_object(self._object_id)
        messages.success(request, self.success_message)
        return redirect(self.redirect_failed_permissions)
