from django.forms import ModelForm
from task_manager.users.models import User


class UserCreateForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'username', 'password']
