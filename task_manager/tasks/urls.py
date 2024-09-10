from django.urls import path
from task_manager.tasks import views

urlpatterns = [
    path('statuses', views.statuses, name='statuses'),

]
