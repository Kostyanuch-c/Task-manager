from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class DataFormMixin:
    """Adds access to the filled attributes to the template"""
    title_form = None
    name_button_in_form = None
    extra_context = {}

    def __init__(self):
        if self.title_form is not None:
            self.extra_context['title_form'] = self.title_form
        if self.name_button_in_form is not None:
            self.extra_context['name_button_in_form'] = self.name_button_in_form


class PermissionsUserChangeMixin:
    """
    Overrides the dispatch method.
    First of all it checks whether the user is authorized.
    And then his rights to change, also adds flash messages
    """
    message_failed_authenticated = _('You are not authorized! Please log in.')
    message_failed_permissions = _("You do not have permission to change another user.")
    redirect_authenticated = reverse_lazy('login')
    redirect_permissions = reverse_lazy('users_list')

    def has_permission(self):
        """ Check if the current user is the object owner """
        return self.get_object() == self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.message_failed_authenticated)
            return redirect(self.redirect_authenticated)
        if not self.has_permission():
            messages.error(request, self.message_failed_permissions)
            return redirect(self.redirect_permissions)
        return super().dispatch(request, *args, **kwargs)
