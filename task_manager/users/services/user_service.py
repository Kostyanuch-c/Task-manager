from django.contrib.auth.hashers import make_password
from django.db import (
    IntegrityError,
    transaction,
)
from django.db.models import ProtectedError
from django.http import Http404

from task_manager.common.base_service import BaseService
from task_manager.users.entities import (
    UserEntity,
    UserInput,
)
from task_manager.users.exceptions import (
    UserDeleteProtectedError,
    UsernameIsNotFreeException,
)
from task_manager.users.models import User
from task_manager.users.repositories.user_repository import UserRepository


class UserService(BaseService):
    def __init__(self):
        self.repository = UserRepository()

    def get_all_objects(self) -> list[UserEntity]:
        return self.repository.get_all_objects()

    def get_object(self, user_id: int) -> UserEntity:
        try:
            return self.repository.get_object(user_id)
        except User.DoesNotExist:
            raise Http404

    def create_object(self, user: UserInput) -> None:
        try:
            with transaction.atomic():
                user.password = make_password(user.password)
                return self.repository.create_object(user)

        except IntegrityError:
            raise UsernameIsNotFreeException

    def update_object(
            self,
            user_id: int,
            user_data: UserInput,
    ) -> None:
        if not self.repository.is_username_free(user_data.username, user_id):
            raise UsernameIsNotFreeException

        user_data.password = make_password(user_data.password)
        self.repository.update_object(user_id, user_data)

    def delete_object(self, user_id: int) -> None:
        try:
            return self.repository.delete_object(user_id)
        except ProtectedError:
            raise UserDeleteProtectedError
