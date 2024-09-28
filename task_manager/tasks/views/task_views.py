from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation.trans_real import gettext as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)

from django_filters.views import FilterView

from task_manager.common.utils import MessagesLoginRequiredMixin
from task_manager.tasks.forms.task_form import (
    TaskFilterForm,
    TaskForm,
)
from task_manager.tasks.models import Task


class TaskDetailView(MessagesLoginRequiredMixin, DetailView):
    template_name = "tasks/task_templates/task_detail.html"
    model = Task

    def get_queryset(self):
        return Task.objects.select_related(
            "status",
            "author",
            "executor",
        ).prefetch_related("labels")

    def get_object(self, queryset=None):
        task_id = self.kwargs.get("pk")
        queryset = self.get_queryset()
        return queryset.get(id=task_id)


class TaskListView(MessagesLoginRequiredMixin, FilterView):
    template_name = "tasks/task_templates/task_list.html"
    model = Task
    filterset_class = TaskFilterForm
    extra_context = {
        "title_list": _("Tasks"),
        "titles_columns": (_("Name"), _("Status"), _("Author"), _("Executor")),
        "create_button_name": _("Create task"),
        "url_to_create": "task_create",
    }

    def get_queryset(self):
        return self.model.objects.select_related(
            "status",
            "author",
            "executor",
        ).prefetch_related("labels")


class TaskCreateView(
    MessagesLoginRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    template_name = "tasks/task_templates/task_create.html"
    form_class = TaskForm
    model = Task
    success_url = reverse_lazy("task_list")
    success_message = _("Task created successfully")

    extra_context = {
        "title_form": _("Create Task"),
        "name_button_in_form": _("Create"),
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(
    MessagesLoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    template_name = "tasks/task_templates/task_update.html"
    form_class = TaskForm
    model = Task
    success_url = reverse_lazy("task_list")
    success_message = _("Task updated successfully")

    extra_context = {
        "title_form": _("Change Task"),
        "name_button_in_form": _("Change"),
    }


class TaskDeleteView(
    UserPassesTestMixin,
    MessagesLoginRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = Task
    template_name = "tasks/task_templates/task_delete.html"
    success_message = _("Task successfully deleted")
    not_permission_message = _("Task can delete only his author")
    success_url = redirect_failed = reverse_lazy("task_list")

    extra_context = {
        "entity_name": _("task"),
        "object_field": "name",
    }

    def get_object(self, queryset=None):
        if not hasattr(self, "_cached_object"):
            self._cached_object = super().get_object(queryset)
        return self._cached_object

    def test_func(self):
        return self.request.user == self.get_object().author
