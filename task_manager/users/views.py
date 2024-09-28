from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.utils.translation.trans_real import gettext as _
from django.contrib import messages
from task_manager.common.utils import MessagesLoginRequiredMixin
from task_manager.users.form import RegisterUserForm


class RegisterUserView(SuccessMessageMixin, CreateView):
    model = get_user_model()
    form_class = RegisterUserForm
    template_name = 'users/user_create_form.html'
    success_url = reverse_lazy('login')
    success_message = _('You have been registered successfully.')

    extra_context = {
        "title_form": _("Registration"),
        "name_button_in_form": _("Register"),
    }


class UsersListView(ListView):
    model = get_user_model()
    template_name = 'users/users_list.html'
    fields = ["username", "full_name"]
    extra_context = {
        "title_list": _("Users"),
        "titles_columns": (_("Name user"), _("Full name")),
        "url_to_update": "update_user",
        "url_to_delete": "delete_user",
        "fields": fields,
    }


class UserUpdateView(UserPassesTestMixin, MessagesLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = get_user_model()
    form_class = RegisterUserForm
    template_name = 'users/user_update_form.html'
    success_url = redirect_failed = reverse_lazy('users_list')
    success_message = _('User successfully changed.')
    not_permission_message = _('You do not have permission to change another user.')
    extra_context = {
        "title_form": _("Edit user"),
        "name_button_in_form": _("Update"),
    }

    def get_object(self, queryset=None):
        if not hasattr(self, '_cached_object'):
            self._cached_object = super().get_object(queryset)
        return self._cached_object

    def test_func(self):
        return self.request.user == self.get_object()


class UserDeleteView(UserPassesTestMixin, MessagesLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = get_user_model()
    success_url = redirect_failed = reverse_lazy('users_list')
    success_message = _('User successfully deleted.')
    not_permission_message = _('You do not have permission to change another user.')
    template_name = "users/user_delete.html"
    extra_context = {
        "entity_name": _("user"),
        "object_field": "full_name",
    }

    def get_object(self, queryset=None):
        if not hasattr(self, '_cached_object'):
            self._cached_object = super().get_object(queryset)
        return self._cached_object

    def test_func(self):
        return self.request.user == self.get_object()

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _("Cannot delete user because it is in use"))
            return redirect(self.redirect_failed)
