from django.contrib.auth import logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from task_manager.users.form import RegisterUserForm


class LoginInView(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('index'))


class RegisterUserView(CreateView):
    model = get_user_model()
    form_class = RegisterUserForm
    template_name = 'users/user_create_form.html'
    success_url = reverse_lazy('login')
