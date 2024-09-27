from django.urls import path

from task_manager.users.views import (
    user_views,
)

urlpatterns = [
    path("", user_views.UsersListView.as_view(), name="users_list"),
    path(
        "create/",
        user_views.RegisterUserView.as_view(),
        name="create_user",
    ),
    path(
        "<int:pk>/update/",
        user_views.UserUpdateView.as_view(),
        name="update_user",
    ),
    path(
        "<int:pk>/delete/",
        user_views.UserDeleteView.as_view(),
        name="delete_user",
    ), ]
