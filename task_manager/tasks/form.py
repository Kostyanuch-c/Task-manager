from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Task


class TaskListForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_button_name = _("Create task")
        self.url_to_create = "task_create"
        self.title_list = _("Tasks")
        self.titles_columns = [
            _("Name"),
            _("Status"),
            _("Author"),
            _("Executor"),
        ]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "status",
            "executor",
            "labels",
        ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.fields[
            "executor"
        ].label_from_instance = lambda user: user.full_name

        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "placeholder": field.label,
                },
            )
