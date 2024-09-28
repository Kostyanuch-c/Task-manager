from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

import django_filters

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


class TaskFilterForm(django_filters.FilterSet):
    executor = django_filters.ModelChoiceFilter(
        queryset=get_user_model().objects.all(),
        label=_("Executor"),
    )
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_("Status"),
    )
    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_("Label"),
        method="filter_by_label",
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "label"]

    def filter_by_label(self, queryset, name, value):
        return queryset.filter(labels__id=value.id)
