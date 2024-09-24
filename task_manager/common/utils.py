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
    """
    Mixin for init service

    Basic mixin for service initialization,
    specifying the service is an integral part of the work of child mixins,
    since all methods are tied to the BaseService abstract class.

    """
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
    """
    Mixin to handle the logic for creating objects.

    Mixin calls the create_object method of the service.
    And passes the flash message

    Works in combination with FormVIew.
    """
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
    """
    Mixin for handling object update

    Mixin, in addition to calling the update_object
    method of the service,
    fills the specified form from form_class by extracting
    data using the get_object method.
    And passes the flash message.

    Like CreateObjectMixin, it works in combination with FormVIew.
    """

    success_message = _("Created successfully")

    def get_initial(self) -> dict[str, Any]:
        entity_object = self.get_object(self.kwargs.get("pk"))

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
    """
    Mixin for handling object deletion

    Mixin calls the delete_object method of the service.
    Redirected and passes the flash message.
    """

    success_message = _("Successfully deleted.")
    url_to = '/'

    def delete(self, request: HttpRequest) -> HttpResponse:
        self.service.delete_object(self.kwargs.get("pk"))
        messages.success(request, self.success_message)
        return redirect(self.url_to)


class CheckPermissionMixin(BaseServiceMixin):
    """
    Mixin for checking user access rights to an object.

    This mixin is used to check if the current user
    has permission to modify a certain object,
    based on the passed object ID and the service logic.
    If the user does not have the necessary rights,
    he will be redirected to the specified URL
    with a message about the lack of rights.

    Also, to use this mixin,
    the service must implement the check_permissions method.

    An exception is the situation of checking the user's
    rights to change their data.
    The user's rights are checked based
    on the belonging of the specified service
    to UserService and a simple comparison of the current user's ID
    with the selected object.
    """

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
    CheckPermissionMixin,
    UpdateObjectMixin,
):
    """Mixin for updating object with permissions check."""


class DeleteWithCheckPermissionsMixin(
    CheckPermissionMixin,
    DeleteObjectMixin,
):
    """Mixin for delete object with permissions check."""
