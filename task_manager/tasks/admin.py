from django.contrib import admin

from task_manager.tasks.models import Task


@admin.register(Task)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "author",
        "executor",
        "status",
    )
