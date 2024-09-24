from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import (
    Label,
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
            "label",
        ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.fields["executor"].label_from_instance = \
            lambda user: user.full_name

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
        queryset=Status.objects.all().only('id', 'name'),
        label=_('Status'),
        required=False,
    )
    executor = forms.ModelChoiceField(
        queryset=get_user_model().objects.all().only(
            "id", "first_name", "last_name",
        ),
        label=_('Executor'),
        required=False,
    )
    label = forms.ModelChoiceField(
        queryset=Label.objects.all().only('id', 'name'),
        label=_('Label'),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["executor"].label_from_instance = \
            lambda user: user.full_name
