from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import BaseForm
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.users.entities import UserOutputEntity as UserEntity
from task_manager.users.exceptions import ServiceNotDefinedError


class MessagesLoginRequiredMixin(LoginRequiredMixin):
    """Mixin for added flash messages in redirect"""

    not_authenticated_message = _("You are not login.")

    def handle_no_permission(self):
        messages.error(self.request, self.not_authenticated_message)
        return redirect(self.get_login_url())


class BaseServiceMixin:
    """Mixin for init service"""

    service = None

    def __init__(self):
        if self.service is None:
            raise ServiceNotDefinedError


class BaseObjectMixin(BaseServiceMixin):
    """Mixin for get  object and object_id"""

    kwargs_key_for_id = "pk"
    _owner_object = None

    def get_from_kwargs_object_id(self, **kwargs):
        """Return the object id from urls params"""
        return kwargs.get(self.kwargs_key_for_id, 0)

    def get_object(self, **kwargs) -> UserEntity:
        """Return object from URL params (loads once)"""
        if self._owner_object is None:
            self._owner_object = self.service.get_object(
                self.get_from_kwargs_object_id(**kwargs),
            )
        return self._owner_object


class CreateObjectMixin(BaseServiceMixin):
    """Mixin to handle the logic for creating or updating objects."""

    success_message = _("Created successfully")

    def mixin_form_valid(
        self,
        request: HttpRequest,
        form: BaseForm,
        object_data: object,
    ) -> HttpResponse:
        self.service.create_object(object_data)
        messages.success(request, self.success_message)
        return super().form_valid(form)


class UpdateObjectMixin(BaseObjectMixin):
    """Mixin for handling object update"""

    success_message = _("Created successfully")

    def mixin_form_valid(
        self,
        request: HttpRequest,
        form: BaseForm,
        object_data: object,
        **kwargs,
    ) -> HttpResponse:
        self.service.update_object(
            self.get_from_kwargs_object_id(**kwargs),
            object_data,
        )

        messages.success(request, self.success_message)
        return super().form_valid(form)


class DeleteObjectMixin(BaseObjectMixin):
    """Mixin for handling object deletion"""

    success_message = _("User successfully deleted.")
    success_url = reverse_lazy("users_list")

    def delete(self, request: HttpRequest, **kwargs) -> HttpResponse:
        self.service.delete_object(self.get_from_kwargs_object_id(**kwargs))
        messages.success(request, self.success_message)
        return redirect(self.success_url)


class PermissionsObjectChangeMixin(BaseObjectMixin):
    """Mixin check permissions for edit object"""

    message_failed_permissions = _(
        "You do not have permission to change another user.",
    )
    redirect_failed = reverse_lazy("users_list")

    def has_permission(
        self, request_user: object, owner_object: UserEntity,
    ) -> bool:  # noqa
        """Check if the current user is the object owner"""
        return owner_object.id == request_user.id

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        request_user = request.user

        if self.get_from_kwargs_object_id(**kwargs) != request_user.id:
            owner_object = self.get_object(**kwargs)
            if not self.has_permission(
                request_user=request_user,
                owner_object=owner_object,
            ):
                messages.error(request, self.message_failed_permissions)
                return redirect(self.redirect_failed)

        return super().dispatch(request, *args, **kwargs)


class UpdateWithPermissionsMixin(
    PermissionsObjectChangeMixin,
    UpdateObjectMixin,
):
    """Mixin for updating object with permissions check."""


class DeleteWithPermissionsMixin(
    PermissionsObjectChangeMixin,
    DeleteObjectMixin,
):
    """Mixin for delete object with permissions check."""
