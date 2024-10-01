from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

import django_filters

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.form.fields[
            "executor"
        ].label_from_instance = lambda user: user.full_name
