from django.contrib.auth.hashers import make_password
from django.db import (
    IntegrityError,
    transaction,
)
from django.utils.translation import gettext_lazy as _

from task_manager.common.base_service import BaseService
from task_manager.users.entities import (
    UserInputEntity,
    UserOutputEntity,
)
from task_manager.users.exceptions import UsernameIsNotFreeException
from task_manager.users.repositories.user_repository import UserRepository


class UserService(BaseService):
    def __init__(self):
        self.repository = UserRepository()

    def get_all_objects(self) -> list[UserOutputEntity]:
        return self.repository.get_all_objects()

    def create_object(self, user: UserInputEntity) -> UserOutputEntity:
        try:
            with transaction.atomic():
                user.password = make_password(user.password)
                return self.repository.create_object(user)

        except IntegrityError:
            raise UsernameIsNotFreeException(_("Username already exists"))

    def update_object(
        self,
        user_id: int,
        user_data: UserInputEntity,
    ) -> None:
        if not self.repository.is_username_free(user_data.username):
            raise UsernameIsNotFreeException(_("Username already exists"))

        user_data.password = make_password(user_data.password)
        self.repository.update_object(user_id, user_data)

    def delete_object(self, user_id: int) -> None:
        return self.repository.delete_object(user_id)

    def get_object(self, user_id: int) -> UserOutputEntity:
        return self.repository.get_object(user_id)
