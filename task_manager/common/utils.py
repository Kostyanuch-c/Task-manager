from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class MessagesLoginRequiredMixin(LoginRequiredMixin):
    not_authenticated_message = _("You are not login.")

    def handle_no_permission(self):
        messages.error(self.request, self.not_authenticated_message)
        return redirect(self.get_login_url())


class LoginRequiredUserTestMixin(
    UserPassesTestMixin, MessagesLoginRequiredMixin,
):
    not_permission_message = _(
        "You do not have permission to change another user.",
    )
    redirect_failed = "/"

    def get_object(self, queryset=None):
        if not hasattr(self, "_cached_object"):
            self._cached_object = super().get_object(queryset)
        return self._cached_object

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        messages.error(self.request, self.not_permission_message)
        return redirect(self.redirect_failed)


class LoginRequiredTaskTestMixin(LoginRequiredUserTestMixin):
    not_permission_message = _("Task can delete only his author")

    def test_func(self):
        return self.request.user == self.get_object().author
