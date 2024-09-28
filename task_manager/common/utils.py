from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class MessagesLoginRequiredMixin(LoginRequiredMixin):
    """Mixin for added flash messages in redirect"""

    not_authenticated_message = _("You are not login.")
    not_permission_message = _("You are not permitted to view this page.")
    redirect_failed = '/'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, self.not_authenticated_message)
            return redirect(self.get_login_url())

        messages.error(self.request, self.not_permission_message)
        return redirect(self.redirect_failed)
