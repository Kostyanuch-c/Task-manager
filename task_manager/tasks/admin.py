from django.contrib import admin

from task_manager.tasks.models import (
    Label,
    Status,
    Task,
)


@admin.register(Task)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "author",
        "executor",
        "status",
    )


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )
