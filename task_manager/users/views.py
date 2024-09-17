from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import (
    redirect,
    render,
)
from django.urls import reverse_lazy
from django.utils.translation.trans_real import gettext as _
from django.views.generic import (
    FormView,
    TemplateView,
)

from task_manager.common.utils import (
    CreateObjectMixin,
    DeleteWithPermissionsMixin,
    MessagesLoginRequiredMixin,
    UpdateWithPermissionsMixin,
)
from task_manager.users.entities import UserInputEntity
from task_manager.users.exceptions import UsernameIsNotFreeException
from task_manager.users.form import RegisterUserForm
from task_manager.users.services.auth_service import AuthService
from task_manager.users.services.user_service import UserService


class IndexView(TemplateView):
    template_name = "index.html"


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
        entity = UserInputEntity(
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
    MessagesLoginRequiredMixin, UpdateWithPermissionsMixin, FormView,
):
    form_class = RegisterUserForm
    template_name = "users/user_update_form.html"

    success_url = reverse_lazy("users_list")
    success_message = _("User updated successfully.")

    extra_context = {
        "title_form": _("Edit user"),
        "name_button_in_form": _("Update"),
    }

    service = UserService()

    def form_valid(self, form: RegisterUserForm) -> HttpResponse:
        entity = UserInputEntity(
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
                **self.kwargs,
            )
        except UsernameIsNotFreeException as exception:
            form.add_error("username", exception.message)
            return self.form_invalid(form)


class UserDeleteView(
    MessagesLoginRequiredMixin, DeleteWithPermissionsMixin, TemplateView,
):
    template_name = "users/user_delete.html"
    success_message = _("User successfully deleted.")

    service = UserService()

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object(**kwargs)
        context["field"] = "full_name"
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return self.delete(request, **kwargs)


class LoginInView(SuccessMessageMixin, FormView):
    form_class = AuthenticationForm
    template_name = "users/login.html"

    success_message = _("You have been logged in.")
    success_url = reverse_lazy("index")

    service = AuthService()

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        if self.service.login_user(request=self.request, **form.cleaned_data):
            return super().form_valid(form)

        return self.form_invalid(form)


def logout_view(request: HttpRequest) -> HttpResponse:
    AuthService().logout_user(request)
    messages.info(request, _("You have been logged out."))
    return redirect(reverse_lazy("index"))


def page_not_found_view(request, exception):
    return render(request, "errors/404.html", status=404)
