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
    DeleteObjectMixin,
    MessagesLoginRequiredMixin,
    UpdateObjectMixin,
)
from task_manager.tasks.entities.status_entity import StatusInput
from task_manager.tasks.exceptions.status_exceptions import (
    StatusDeleteProtectedError,
    StatusTitleIsNotFreeException,
)
from task_manager.tasks.forms.status_form import StatusForm
from task_manager.tasks.services.status_service import StatusService


class StatusListView(MessagesLoginRequiredMixin, TemplateView):
    template_name = "tasks/statuses/status_list.html"

    extra_context = {
        "title_list": _("Statuses"),
        "titles_columns": (_("Name"),),
        "create_button_name": _("Create status"),
        "url_to_create": "status_create",
        "url_to_update": "status_update",
        "url_to_delete": "status_delete",
        "fields": ("name",),
    }

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["object_list"] = StatusService().get_all_objects()
        return context


class StatusCreateView(MessagesLoginRequiredMixin, CreateObjectMixin, FormView):
    template_name = "tasks/statuses/status_create.html"
    form_class = StatusForm

    success_url = reverse_lazy("status_list")
    success_message = _("Status successfully created.")

    extra_context = {
        "title_form": _("Create Status"),
        "name_button_in_form": _("Create"),
    }

    service = StatusService()

    def form_valid(self, form: StatusForm) -> HttpResponse:
        entity = StatusInput(form.cleaned_data["name"])
        try:
            return self.mixin_form_valid(
                request=self.request,
                form=form,
                object_data=entity,
            )
        except StatusTitleIsNotFreeException as exception:
            form.add_error("name", exception.message)
            return self.form_invalid(form)


class StatusUpdateView(MessagesLoginRequiredMixin, UpdateObjectMixin, FormView):
    template_name = "tasks/statuses/status_update.html"
    form_class = StatusForm

    success_url = reverse_lazy("status_list")
    success_message = _("Status successfully updated.")

    extra_context = {
        "title_form": _("Edit Status"),
        "name_button_in_form": _("Update"),
    }

    service = StatusService()

    def form_valid(self, form: StatusForm) -> HttpResponse:
        entity = StatusInput(form.cleaned_data["name"])
        try:
            return self.mixin_form_valid(
                request=self.request,
                form=form,
                object_data=entity,
                **self.kwargs,
            )
        except StatusTitleIsNotFreeException as exception:
            form.add_error("name", exception.message)
            return self.form_invalid(form)


class StatusDeleteView(
    MessagesLoginRequiredMixin,
    DeleteObjectMixin,
    TemplateView,
):
    template_name = "tasks/statuses/status_delete.html"
    success_message = _("Status successfully deleted.")
    url_to = reverse_lazy("status_list")

    extra_context = {
        "entity_name": _("as status"),
    }

    service = StatusService()

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["object_name"] = self.get_object(**kwargs).name
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            return self.delete(request, **kwargs)
        except StatusDeleteProtectedError as exception:
            messages.error(request, exception.message)
            return redirect(self.url_to)
