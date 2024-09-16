from django.contrib import admin

from task_manager.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "date_joined",
        "is_active",
        "is_staff",
    )
