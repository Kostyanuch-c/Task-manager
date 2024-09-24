from django.contrib import messages
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

from task_manager.common.utils import (
    CreateObjectMixin,
    DeleteWithCheckPermissionsMixin,
    MessagesLoginRequiredMixin,
    UpdateWithCheckPermissionsMixin,
)
from task_manager.users.entities import UserInput
from task_manager.users.exceptions import (
    UserDeleteProtectedError,
    UsernameIsNotFreeException,
)
from task_manager.users.form import RegisterUserForm
from task_manager.users.services.user_service import UserService


class UsersListView(TemplateView):
    template_name = "users/users_list.html"
    fields = ["username", "full_name"]
    extra_context = {
        "title_list": _("Users"),
        "titles_columns": (_("Name user"), _("Full name")),
        "url_to_update": "update_user",
        "url_to_delete": "delete_user",
        "fields": fields,
    }

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["object_list"] = UserService().get_all_objects()
        return context


class RegisterUserView(CreateObjectMixin, FormView):
    template_name = "users/user_create_form.html"
    form_class = RegisterUserForm

    success_url = reverse_lazy("login")
    success_message = _("You have been registered successfully.")

    extra_context = {
        "title_form": _("Registration"),
        "name_button_in_form": _("Register"),
    }

    service = UserService()

    def form_valid(self, form: RegisterUserForm) -> HttpResponse:
        entity = UserInput(
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        try:
            return self.mixin_form_valid(
                request=self.request,
                form=form,
                object_data=entity,
            )
        except UsernameIsNotFreeException as exception:
            form.add_error("username", exception.message)
            return self.form_invalid(form)


class UserUpdateView(
    MessagesLoginRequiredMixin,
    UpdateWithCheckPermissionsMixin,
    FormView,
):
    template_name = "users/user_update_form.html"

    success_url = redirect_failed = reverse_lazy("users_list")
    success_message = _("User updated successfully.")
    message_failed_permissions = _(
        "you do not have permission to change another user",
    )

    extra_context = {
        "title_form": _("Edit user"),
        "name_button_in_form": _("Update"),
    }

    service = UserService()
    form_class = RegisterUserForm

    def form_valid(self, form: RegisterUserForm) -> HttpResponse:
        entity = UserInput(
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        try:
            return self.mixin_form_valid(
                request=self.request,
                form=form,
                object_data=entity,
            )
        except UsernameIsNotFreeException as exception:
            form.add_error("username", exception.message)
            return self.form_invalid(form)


class UserDeleteView(
    MessagesLoginRequiredMixin,
    DeleteWithCheckPermissionsMixin,
    TemplateView,
):
    template_name = "users/user_delete.html"
    success_message = _("User successfully deleted.")
    url_to = redirect_failed = reverse_lazy("users_list")
    message_failed_permissions = _(
        "You do not have permission to change another user",
    )
    extra_context = {
        "entity_name": _("user"),
    }

    service = UserService()

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["object_name"] = self.request.user.full_name
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            return self.delete(request)
        except UserDeleteProtectedError as exception:
            messages.error(request, exception.message)
            return redirect(self.url_to)
