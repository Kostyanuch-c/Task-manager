from django.forms import ModelForm, CharField, PasswordInput, RegexField
from task_manager.users.models import User
from django.utils.translation import gettext_lazy as _


class UserCreateForm(ModelForm):
    confirm_password = CharField(
        label=_('Confirm password'),
        help_text=_('To confirm your entry, please enter the password again.'),
        widget=PasswordInput()
    )

    class Meta:
        model = User
        fields = ['name', 'surname', 'username', 'password', 'confirm_password']
        widgets = {'password': PasswordInput()}

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'placeholder': field.label,
            })

    def clean(self) -> None:
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', _('passwords do not match'))
