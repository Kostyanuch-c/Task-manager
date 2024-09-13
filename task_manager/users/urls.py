from django.urls import path

from task_manager.users import views


urlpatterns = [
    path('login/', views.LoginInView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.UsersListView.as_view(), name='users_list'),
    path('users/create/', views.RegisterUserView.as_view(), name='create_user'),
    path(
        'users/<int:pk>/update', views.UserUpdateView.as_view(),
        name='update_user',
    ),
    path(
        'users/<int:pk>/delete', views.UserDeleteView.as_view(),
        name='delete_user',
    ),
]
