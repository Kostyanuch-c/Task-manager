from django.views.generic import CreateView

from task_manager.users.models import User
from task_manager.users.form import UserCreateForm


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name_suffix = '_create_form'
