from django.urls import path

from task_manager.tasks.views import statuses_views


urlpatterns = [
    path("", statuses_views.StatusListView.as_view(), name="status_list"),
    path(
        "create/",
        statuses_views.StatusCreateView.as_view(),
        name="status_create",
    ),
    path(
        "<int:pk>/update/",
        statuses_views.StatusUpdateView.as_view(),
        name="status_update",
    ),
    path(
        "<int:pk>/delete/",
        statuses_views.StatusDeleteView.as_view(),
        name="status_delete",
    ),
]
