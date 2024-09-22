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
from task_manager.tasks.entities.label_entity import LabelInput
from task_manager.tasks.exceptions.label_exceptions import (
    LabelDeleteProtectedError,
    LabelNameIsNotFreeException,
)
from task_manager.tasks.forms.label_form import LabelForm
from task_manager.tasks.services.label_service import LabelService


class LabelListView(MessagesLoginRequiredMixin, TemplateView):
    template_name = "tasks/labels/label_list.html"

    extra_context = {
        "title_list": _("Labels"),
        "titles_columns": (_("Name"),),
        "create_button_name": _("Create label"),
        "url_to_create": "label_create",
        "url_to_update": "label_update",
        "url_to_delete": "label_delete",
        "fields": ("name",),
    }

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['object_list'] = LabelService().get_all_objects()
        return context


class LabelCreateView(MessagesLoginRequiredMixin, CreateObjectMixin, FormView):
    template_name = "tasks/labels/label_create.html"
    form_class = LabelForm

    success_url = reverse_lazy("label_list")
    success_message = _("Label successfully created.")

    extra_context = {
        "title_form": _("Create Label"),
        "name_button_in_form": _("Create"),
    }

    service = LabelService()

    def form_valid(self, form: LabelForm) -> HttpResponse:
        entity = LabelInput(form.cleaned_data["name"])
        try:
            return self.mixin_form_valid(
                request=self.request,
                form=form,
                object_data=entity,
            )
        except LabelNameIsNotFreeException as exception:
            form.add_error("name", exception.message)
            return self.form_invalid(form)


class LabelUpdateView(MessagesLoginRequiredMixin, UpdateObjectMixin, FormView):
    template_name = "tasks/labels/label_update.html"
    form_class = LabelForm

    success_url = reverse_lazy("label_list")
    success_message = _("Label successfully updated.")

    extra_context = {
        "title_form": _("Edit label"),
        "name_button_in_form": _("Update"),
    }

    service = LabelService()

    def form_valid(self, form: LabelForm) -> HttpResponse:
        entity = LabelInput(form.cleaned_data["name"])
        try:
            return self.mixin_form_valid(
                request=self.request,
                form=form,
                object_data=entity,
                **self.kwargs,
            )
        except LabelNameIsNotFreeException as exception:
            form.add_error("name", exception.message)
            return self.form_invalid(form)


class LabelDeleteView(
    MessagesLoginRequiredMixin,
    DeleteObjectMixin,
    TemplateView,
):
    template_name = "tasks/labels/label_delete.html"
    success_message = _("Label successfully deleted.")
    url_to = reverse_lazy("label_list")

    extra_context = {
        "entity_name": _("label's"),
    }

    service = LabelService()

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["object_name"] = self.get_object(**kwargs).name
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            return self.delete(request, **kwargs)
        except LabelDeleteProtectedError as exception:
            messages.error(request, exception.message)
            return redirect(self.url_to)
