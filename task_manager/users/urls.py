from django.urls import path

from task_manager.users.views import (
    auth_views,
    user_views,
)


urlpatterns = [
    path("", auth_views.IndexView.as_view(), name="index"),
    path("login/", auth_views.LoginInView.as_view(), name="login"),
    path("logout/", auth_views.logout_view, name="logout"),
    path("users/", user_views.UsersListView.as_view(), name="users_list"),
    path(
        "users/create/",
        user_views.RegisterUserView.as_view(),
        name="create_user",
    ),
    path(
        "users/<int:pk>/update/",
        user_views.UserUpdateView.as_view(),
        name="update_user",
    ),
    path(
        "users/<int:pk>/delete/",
        user_views.UserDeleteView.as_view(),
        name="delete_user",
    ),
]
