from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from task_manager.common.base_repositories import BaseRepository
from task_manager.users.entities import (
    UserEntity,
    UserInput,
)


class UserRepository(BaseRepository):
    def __init__(self):
        self.user = get_user_model()

    def is_username_free(self, username: str) -> bool:
        return not self.user.objects.filter(username=username).exists()

    def get_all_objects(self) -> list[UserEntity]:
        queryset = self.user.objects.all()
        return [user.to_entity() for user in queryset]

    def create_object(self, user: UserInput) -> UserEntity:
        queryset = self.user.objects.create(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            password=user.password,
        )
        return queryset.to_entity()

    def update_object(self, user_id: int, user_data: UserInput) -> None:
        self.user.objects.filter(id=user_id).update(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username,
            password=user_data.password,
        )

    def delete_object(self, user_id: int) -> None:
        self.user.objects.filter(id=user_id).delete()

    def get_object(self, user_id: int) -> UserEntity:
        return get_object_or_404(self.user, id=user_id).to_entity()
