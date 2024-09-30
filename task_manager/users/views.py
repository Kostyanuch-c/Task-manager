from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation.trans_real import gettext as _
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from task_manager.common.utils import LoginRequiredUserTestMixin
from task_manager.users.form import (
    RegisterUserForm,
    UserListForm,
)


class RegisterUserView(SuccessMessageMixin, CreateView):
    model = get_user_model()
    form_class = RegisterUserForm
    template_name = "users/user_create_form.html"
    success_url = reverse_lazy("login")
    success_message = _("You have been registered successfully.")

    extra_context = {
        "title_form": _("Registration"),
        "name_button_in_form": _("Register"),
    }


class UsersListView(ListView):
    model = get_user_model()
    template_name = "users/users_list.html"
    extra_context = {
        "form": UserListForm,
    }


class UserUpdateView(
    LoginRequiredUserTestMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = get_user_model()
    form_class = RegisterUserForm
    template_name = "users/user_update_form.html"
    success_url = redirect_failed = reverse_lazy("users_list")
    success_message = _("User successfully changed.")

    extra_context = {
        "title_form": _("Edit user"),
        "name_button_in_form": _("Update"),
    }


class UserDeleteView(
    LoginRequiredUserTestMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = get_user_model()
    success_url = redirect_failed = reverse_lazy("users_list")
    success_message = _("User successfully deleted.")

    template_name = "users/user_delete.html"
    extra_context = {
        "entity_name": _("user"),
        "object_field": "full_name",
    }

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                _("Cannot delete user because it is in use"),
            )
            return redirect(self.redirect_failed)
