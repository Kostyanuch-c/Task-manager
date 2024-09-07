from django.urls import path
from task_manager.users import views

urlpatterns = [
    path('create/', views.UserCreateView.as_view(), name='create_user'),
]
