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

    kwargs_key_for_id = "pk"
    service = None
    _object_id = None
    _cached_object = None

    def __init__(self):
        if self.service is None:
            raise ServiceNotDefinedError

    def get_from_kwargs_object_id(self, **kwargs):
        if self._object_id is None:
            self._object_id = kwargs.get(self.kwargs_key_for_id, 0)
        return self._object_id

    def get_object(self, **kwargs):
        if self._cached_object is None:
            self._cached_object = self.service.repository.get_object(
                self.get_from_kwargs_object_id(**kwargs),
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


class DeleteObjectMixin(BaseServiceMixin):
    """Mixin for handling object deletion"""

    success_message = _("User successfully deleted.")
    url_to = reverse_lazy("users_list")

    def delete(self, request: HttpRequest, **kwargs) -> HttpResponse:
        self.service.delete_object(self.get_from_kwargs_object_id(**kwargs))
        messages.success(request, self.success_message)
        return redirect(self.url_to)


class CheckMixin(BaseServiceMixin):
    message_failed_permissions = _("You do not have permission to change")
    redirect_failed = "/"
    _has_permission = False

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        object_id = self.get_from_kwargs_object_id(**kwargs)

        if isinstance(self.service, UserService):
            self._has_permission = request.user.id == object_id
        else:
            object_ = self.get_object(**kwargs)
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
