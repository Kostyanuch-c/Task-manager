from django.forms import (
    Form,
    ModelForm,
    TextInput,
)
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label


class LabelListForm(Form):
    def __init__(self, *args, **kwargs):
        self.create_button_name = (_("Create label"),)
        self.url_to_update = "label_update"
        self.url_to_delete = "label_delete"
        self.url_to_create = "label_create"
        self.title_list = (_("Labels"),)
        self.titles_columns = ((_("Name"),),)
        self.attrs = ["id", "name", "created_at"]

        super().__init__(*args, **kwargs)


class LabelForm(ModelForm):
    class Meta:
        model = Label
        fields = ("name",)
        widgets = {
            "name": TextInput(attrs={"placeholder": _("Name")}),
        }
