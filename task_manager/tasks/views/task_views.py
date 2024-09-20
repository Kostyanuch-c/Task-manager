from django.http import HttpResponse
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
    UpdateObjectMixin,
)
from task_manager.tasks.entities.converters import TaskEntityConverter
from task_manager.tasks.entities.task_entity import TaskInput
from task_manager.tasks.exceptions.task_exceptions import (
    TaskNameIsNotFreeException,
)
from task_manager.tasks.forms.task_form import (
    TaskFilterForm,
    TaskForm,
)
from task_manager.tasks.services.task_service import TaskService


class TaskDetailView(MessagesLoginRequiredMixin, TemplateView):
    template_name = "tasks/task_templates/task_detail.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        task_entity = TaskService().get_object(kwargs.get("pk"))
        context["object"] = TaskEntityConverter.to_output_template(task_entity)
        return context


class TaskListView(MessagesLoginRequiredMixin, TemplateView):
    template_name = "tasks/task_templates/task_list.html"

    fields = ("name", "status_name", "author_full_name", "performer_full_name")
    extra_context = {
        "title_list": _("Tasks"),
        "titles_columns": (_("Name"), _("Status"), _("Author"), _("Performer")),
        "create_button_name": _("Create task"),
        "url_to_detail": "task_detail",
        "url_to_create": "task_create",
        "url_to_update": "task_update",
        "url_to_delete": "task_delete",
        "fields": fields,
    }

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET

        context["form"] = TaskFilterForm(query_params)
        task_entities = TaskService().get_all_objects(
            query_params=query_params,
            user_id=self.request.user.id,
        )
        context["object_list"] = TaskEntityConverter.to_output_list(
            task_entities,
        )

        return context


class TaskCreateView(MessagesLoginRequiredMixin, CreateObjectMixin, FormView):
    template_name = "tasks/task_templates/task_create.html"
    form_class = TaskForm

    success_url = reverse_lazy("task_list")
    success_message = _("Task created successfully")

    extra_context = {
        "title_form": _("Create Task"),
        "name_button_in_form": _("Create"),
    }

    service = TaskService()

    def form_valid(self, form: TaskForm) -> HttpResponse:
        entity = TaskInput(
            name=form.cleaned_data["name"],
            description=form.cleaned_data["description"],
            status=form.cleaned_data["status"],
            performer=form.cleaned_data["performer"],
            author=self.request.user,
        )

        try:
            return self.mixin_form_valid(
                request=self.request,
                form=form,
                object_data=entity,
            )
        except TaskNameIsNotFreeException as exception:
            form.add_error("name", exception.message)
            return self.form_invalid(form)


class TaskUpdateView(MessagesLoginRequiredMixin, UpdateObjectMixin, FormView):
    template_name = "tasks/task_templates/task_update.html"
    form_class = TaskForm

    success_url = reverse_lazy("task_list")
    success_message = _("Task updated successfully")

    extra_context = {
        "title_form": _("Change Task"),
        "name_button_in_form": _("Change"),
    }

    service = TaskService()

    def form_valid(self, form: TaskForm) -> HttpResponse:
        entity = TaskInput(
            name=form.cleaned_data["name"],
            description=form.cleaned_data["description"],
            status=form.cleaned_data["status"],
            performer=form.cleaned_data["performer"],
            author=self.request.user,
        )

        try:
            return self.mixin_form_valid(
                request=self.request,
                form=form,
                object_data=entity,
                **self.kwargs,
            )
        except TaskNameIsNotFreeException as exception:
            form.add_error("name", exception.message)
            return self.form_invalid(form)


class TaskDeleteView(
    MessagesLoginRequiredMixin,
    DeleteWithCheckPermissionsMixin,
    TemplateView,
):
    template_name = "tasks/task_templates/task_delete.html"
    success_message = _("Task successfully deleted")
    message_failed_permissions = _("Task can delete only his author")

    url_to = redirect_failed = reverse_lazy("task_list")

    extra_context = {
        "entity_name": _("task"),
    }

    service = TaskService()

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["object_name"] = self.get_object(**kwargs).name
        return context

    def post(self, request, *args, **kwargs):
        return self.delete(request, **kwargs)
