from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput


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
