from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from task_manager.users.entities import (
    User as UserEntity,
    UserChangeOrCreate,
)


class UserRepository:
    def __init__(self):
        self.user = get_user_model()

    def is_username_free(self, username: str) -> bool:
        return not self.user.objects.filter(username=username).exists()

    def get_all_users(self) -> list[UserEntity]:
        queryset = self.user.objects.all()
        return [user.to_entity() for user in queryset]

    def create_user(self, user: UserChangeOrCreate) -> UserEntity:
        queryset = self.user.objects.create(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            password=user.password,
        )
        return queryset.to_entity()

    def update_user(self, user_id: int, user_data: UserChangeOrCreate) -> None:
        user = self.user.objects.get(id=user_id)

        if self.is_username_free(user_data.username):
            user.first_name = user_data.first_name
            user.last_name = user_data.last_name
            user.username = user_data.username
            user.password = user_data.password
            user.save()
        else:
            raise IntegrityError("Username is already taken.")

    def delete_user(self, user_id: int) -> None:
        self.user.objects.filter(id=user_id).delete()

    def get_user(self, user_id: int) -> UserEntity:
        user = get_object_or_404(self.user, id=user_id)
        return user.to_entity()
