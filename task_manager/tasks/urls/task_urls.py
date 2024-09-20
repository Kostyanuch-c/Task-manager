from django.urls import path

from task_manager.tasks.views import task_views


urlpatterns = [
    path("", task_views.TaskListView.as_view(), name="task_list"),
    path(
        "create/",
        task_views.TaskCreateView.as_view(),
        name="task_create",
    ),
    path("<int:pk>/", task_views.TaskDetailView.as_view(), name="task_detail"),
    path(
        "<int:pk>/update/",
        task_views.TaskUpdateView.as_view(),
        name="task_update",
    ),
    path(
        "<int:pk>/delete/",
        task_views.TaskDeleteView.as_view(),
        name="task_delete",
    ),
]
