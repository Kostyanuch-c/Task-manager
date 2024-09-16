from django.contrib.auth.hashers import make_password
from django.db import (
    IntegrityError,
    transaction,
)
from django.utils.translation import gettext_lazy as _

from task_manager.users.entities import (
    User as UserEntity,
    UserChangeOrCreate,
)
from task_manager.users.exceptions import UsernameIsNotFreeException
from task_manager.users.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_all_objects(self) -> list[UserEntity]:
        return self.user_repository.get_all_users()

    def create_object(self, user: UserChangeOrCreate) -> UserEntity:
        try:
            with transaction.atomic():
                user.password = make_password(user.password)
                return self.user_repository.create_user(user)

        except IntegrityError:
            raise UsernameIsNotFreeException(_("Username already exists"))

    def update_object(
        self,
        user_id: int,
        user_data: UserChangeOrCreate,
    ) -> None:
        try:
            with transaction.atomic():
                user_data.password = make_password(user_data.password)
                self.user_repository.update_user(user_id, user_data)
                transaction.on_commit(
                    lambda: print("Data committed successfully"),
                )
        except IntegrityError:
            raise UsernameIsNotFreeException(_("Username already exists"))

    def delete_object(self, user_id: int) -> None:
        return self.user_repository.delete_user(user_id)

    def get_object(self, user_id: int) -> UserEntity:
        return self.user_repository.get_user(user_id)
