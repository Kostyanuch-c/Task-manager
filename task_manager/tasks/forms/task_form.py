from django.forms import ModelForm

from task_manager.tasks.models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "status",
            "performer",
        ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "placeholder": field.label,
                },
            )

    def validate_unique(self):
        pass
