from collections.abc import Iterable

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from task_manager.users.entities import (
    User as UserEntity,
    UserCreate,
)


class UserRepository:
    def is_username_free(self, username: str) -> bool:
        return not get_user_model().objects.filter(username=username).exists()

    def get_all_users(self) -> Iterable[UserEntity]:
        queryset = get_user_model().objects.all()
        return [user.to_entity() for user in queryset]

    def create_user(self, user: UserCreate) -> UserEntity:
        queryset = get_user_model().objects.create(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            password=user.password,
        )
        return queryset.to_entity()

    def update_user(self, user: UserCreate) -> None:
        if self.is_username_free(user.username):
            get_user_model().objects.filter(username=user.username).update(
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                password=user.password,
            )
        else:
            raise IntegrityError

    def delete_user(self, user_id: int) -> None:
        get_user_model().objects.filter(id=user_id).delete()

    def get_user(self, user_id: int) -> UserEntity:
        user = get_object_or_404(get_user_model(), id=user_id)
        return user.to_entity()
