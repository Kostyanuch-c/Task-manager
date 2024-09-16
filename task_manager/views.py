from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


def page_not_found_view(request, exception):
    return render(request, "errors/404.html", status=404)
