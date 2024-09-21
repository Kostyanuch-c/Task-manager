from django import forms
from django.contrib.auth import get_user_model

from task_manager.tasks.models import (
    Status,
    Task,
)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "status",
            "executor",
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


class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(), required=False,
    )
    executor = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["executor"].label_from_instance = lambda obj: obj.full_name
