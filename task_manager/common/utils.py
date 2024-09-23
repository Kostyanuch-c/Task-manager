from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import BaseForm
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from task_manager.users.exceptions import ServiceNotDefinedError
from task_manager.users.services.user_service import UserService


class MessagesLoginRequiredMixin(LoginRequiredMixin):
    """Mixin for added flash messages in redirect"""

    not_authenticated_message = _("You are not login.")

    def handle_no_permission(self):
        messages.error(self.request, self.not_authenticated_message)
        return redirect(self.get_login_url())


class BaseServiceMixin:
    """Mixin for init service"""

    service = None
    _cached_object = None

    def __init__(self):
        if self.service is None:
            raise ServiceNotDefinedError

    def get_object(self, object_id: int):
        if self._cached_object is None:
            self._cached_object = self.service.repository.get_object(
                object_id,
            )
        return self._cached_object


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


class UpdateObjectMixin(BaseServiceMixin):
    """Mixin for handling object update"""

    success_message = _("Created successfully")

    def get_initial(self) -> dict[str, Any]:
        entity_object = self.service.get_object(self.kwargs.get("pk"))

        initial = {
            key: value
            if not callable(value)
            else value.all()
            for key, value in entity_object.__dict__.items()
            if key not in ('id', 'created_at')
        }

        return initial

    def mixin_form_valid(
            self,
            request: HttpRequest,
            form: BaseForm,
            object_data: object,
    ) -> HttpResponse:
        self.service.update_object(
            self.kwargs.get("pk"),
            object_data,
        )

        messages.success(request, self.success_message)
        return super().form_valid(form)


class DeleteObjectMixin(BaseServiceMixin):
    """Mixin for handling object deletion"""

    success_message = _("Successfully deleted.")
    url_to = '/'

    def delete(self, request: HttpRequest) -> HttpResponse:
        self.service.delete_object(self.kwargs.get("pk"))
        messages.success(request, self.success_message)
        return redirect(self.url_to)


class CheckMixin(BaseServiceMixin):
    message_failed_permissions = _("You do not have permission to change")
    redirect_failed = "/"
    _has_permission = False

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        object_id = self.kwargs.get("pk")

        if isinstance(self.service, UserService):
            self._has_permission = request.user.id == object_id
        else:
            object_ = self.get_object(object_id)
            self._has_permission = self.service.check_permissions(
                request.user,
                object_,
            )

        if not self._has_permission:
            messages.error(request, self.message_failed_permissions)
            return redirect(self.redirect_failed)

        return super().dispatch(request, *args, **kwargs)


class UpdateWithCheckPermissionsMixin(
    CheckMixin,
    UpdateObjectMixin,
):
    """Mixin for updating object with permissions check."""


class DeleteWithCheckPermissionsMixin(
    CheckMixin,
    DeleteObjectMixin,
):
    """Mixin for delete object with permissions check."""
