from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput
from django.utils.translation.trans_real import gettext as _


class UserListForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.url_to_update = "update_user"
        self.url_to_delete = "delete_user"
        self.title_list = _("Users")
        self.titles_columns = (_("Name user"), _("Full name"))
        self.attrs = ["id", "username", "full_name", "date_joined"]

        super().__init__(*args, **kwargs)


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        ]

        widgets = {
            "first_name": TextInput(attrs={"required": True}),
            "last_name": TextInput(attrs={"required": True}),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "placeholder": field.label,
                },
            )
