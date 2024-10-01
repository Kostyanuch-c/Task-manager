from django.contrib import messages
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

from task_manager.common.mixin import MessagesLoginRequiredMixin
from task_manager.statuses.form import (
    StatusForm,
    StatusListForm,
)
from task_manager.statuses.models import Status


class StatusListView(MessagesLoginRequiredMixin, ListView):
    template_name = "statuses/status_list.html"
    model = Status

    extra_context = {
        "form": StatusListForm,
    }


class StatusCreateView(
    MessagesLoginRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    template_name = "statuses/status_create.html"
    form_class = StatusForm
    model = Status
    success_url = reverse_lazy("status_list")
    success_message = _("Status successfully created.")

    extra_context = {
        "title_form": _("Create Status"),
        "name_button_in_form": _("Create"),
    }


class StatusUpdateView(
    MessagesLoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    template_name = "statuses/status_update.html"
    form_class = StatusForm
    model = Status
    success_url = reverse_lazy("status_list")
    success_message = _("Status successfully updated.")

    extra_context = {
        "title_form": _("Edit Status"),
        "name_button_in_form": _("Update"),
    }


class StatusDeleteView(
    MessagesLoginRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = Status
    template_name = "statuses/status_delete.html"
    success_message = _("Status successfully deleted.")
    success_url = reverse_lazy("status_list")

    extra_context = {
        "entity_name": _("as status"),
        "object_field": "name",
    }

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                _("Cannot delete status because it is in use"),
            )
            return redirect(self.success_url)
