from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordMixin
from django.core.validators import MinLengthValidator
from django.forms import CharField, PasswordInput, ModelForm
from django.utils.translation import gettext_lazy as _


class RegisterUserForm(SetPasswordMixin, ModelForm):
    password1 = CharField(
        label=_('Password'),
        widget=PasswordInput(),
        validators=[MinLengthValidator(3, message=_('Password must be at least 3 characters long.'))],
        help_text=_('Password must be at least 3 characters long.'),
    )
    password2 = CharField(
        label=_('Confirm password'),
        help_text=_('To confirm your entry, please enter the password again.'),
        widget=PasswordInput(),
    )

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'placeholder': field.label,
            })

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', _('passwords do not match'))

    def save(self, commit=True):
        user = super().save(commit=False)
        user = self.set_password_and_save(user, commit=commit)
        if commit and hasattr(self, "save_m2m"):
            self.save_m2m()
        return user
