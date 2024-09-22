from django.urls import path

from task_manager.tasks.views import label_views


urlpatterns = [
    path("", label_views.LabelListView.as_view(), name="label_list"),
    path(
        "create/",
        label_views.LabelCreateView.as_view(),
        name="label_create",
    ),
    path(
        "<int:pk>/update/",
        label_views.LabelUpdateView.as_view(),
        name="label_update",
    ),
    path(
        "<int:pk>/delete/",
        label_views.LabelDeleteView.as_view(),
        name="label_delete",
    ),
]
