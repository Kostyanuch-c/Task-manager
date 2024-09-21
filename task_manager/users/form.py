from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.forms import (
    CharField,
    ModelForm,
    PasswordInput,
    TextInput,
)
from django.utils.translation import gettext_lazy as _


class RegisterUserForm(ModelForm):
    password1 = CharField(
        label=_('Password'),
        widget=PasswordInput(),
        validators=[
            MinLengthValidator(
                3,
                message=_('Password must be at least 3 characters long.'),
            ),
        ],
        help_text=_('Password must be at least 3 characters long.'),
    )
    password2 = CharField(
        label=_('Confirm password'),
        help_text=_('To confirm your entry, please enter the password again.'),
        widget=PasswordInput(),
    )

    class Meta:
        model = get_user_model()
        fields = [
            'first_name', 'last_name',
            'username', 'password1', 'password2',
        ]

        widgets = {
            'first_name': TextInput(attrs={'required': True}),
            'last_name': TextInput(attrs={'required': True}),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'placeholder': field.label,
            })

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', _('passwords do not match'))

    def validate_unique(self):
        pass
