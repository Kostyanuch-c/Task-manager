from django.urls import path
from task_manager.users import views

urlpatterns = [
    path('users/create/', views.RegisterUserView.as_view(), name='create_user'),
    path('login/', views.LoginInView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.GetUsersView.as_view(), name='users_list'),
]
