from django.forms import (
    Form,
    ModelForm,
    TextInput,
)
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status


class StatusListForm(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_button_name = _("Create status")
        self.url_to_update = "status_update"
        self.url_to_delete = "status_delete"
        self.url_to_create = "status_create"
        self.title_list = _("Statuses")
        self.titles_columns = (_("Name"),)
        self.attrs = ["id", "name", "created_at"]


class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ("name",)
        widgets = {
            "name": TextInput(attrs={"placeholder": _("Name")}),
        }
