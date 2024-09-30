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

from task_manager.common.utils import (
    LoginRequiredTaskTestMixin,
    MessagesLoginRequiredMixin,
)
from task_manager.tasks.form import (
    TaskFilterForm,
    TaskForm,
    TaskListForm,
)
from task_manager.tasks.models import Task


class TaskDetailView(MessagesLoginRequiredMixin, DetailView):
    template_name = "tasks/task_detail.html"
    model = Task


class TaskListView(MessagesLoginRequiredMixin, FilterView):
    template_name = "tasks/task_list.html"
    model = Task
    filterset_class = TaskFilterForm
    extra_context = {
        "form": TaskListForm,
    }


class TaskCreateView(
    MessagesLoginRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    template_name = "tasks/task_create.html"
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
    template_name = "tasks/task_update.html"
    form_class = TaskForm
    model = Task
    success_url = reverse_lazy("task_list")
    success_message = _("Task updated successfully")

    extra_context = {
        "title_form": _("Change Task"),
        "name_button_in_form": _("Change"),
    }


class TaskDeleteView(
    LoginRequiredTaskTestMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = Task
    template_name = "tasks/task_delete.html"
    success_message = _("Task successfully deleted")

    success_url = redirect_failed = reverse_lazy("task_list")

    extra_context = {
        "entity_name": _("task"),
        "object_field": "name",
    }
