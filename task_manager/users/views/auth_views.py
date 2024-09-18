from http import HTTPStatus

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import (
    redirect,
    render,
)
from django.urls import reverse_lazy
from django.utils.translation.trans_real import gettext as _
from django.views.generic import (
    FormView,
    TemplateView,
)

from task_manager.users.services.auth_service import AuthService


class IndexView(TemplateView):
    template_name = "index.html"


class LoginInView(SuccessMessageMixin, FormView):
    form_class = AuthenticationForm
    template_name = "users/login.html"

    success_message = _("You have been logged in.")
    success_url = reverse_lazy("index")

    service = AuthService()

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        if self.service.login_user(request=self.request, **form.cleaned_data):
            return super().form_valid(form)

        return self.form_invalid(form)


def logout_view(request: HttpRequest) -> HttpResponse:
    AuthService().logout_user(request)
    messages.info(request, _("You have been logged out."))
    return redirect(reverse_lazy("index"))


def page_not_found_view(request, exception):
    return render(request, "errors/404.html", status=HTTPStatus.NOT_FOUND)
