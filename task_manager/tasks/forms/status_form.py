from django.forms import (
    ModelForm,
    TextInput,
)
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Status


class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ("title",)
        widgets = {
            "title": TextInput(attrs={"placeholder": _("Name")}),
        }
