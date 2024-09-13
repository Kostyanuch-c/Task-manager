from collections.abc import Iterable

from django.contrib.auth.hashers import make_password
from django.db import (
    IntegrityError,
    transaction,
)
from django.utils.translation import gettext_lazy as _

from task_manager.users.entities import (
    User as UserEntity,
    UserCreate,
)
from task_manager.users.exceptions import UsernameIsNotFreeError
from task_manager.users.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_all_users(self) -> Iterable[UserEntity]:
        return self.user_repository.get_all_users()

    def register_user(self, user: UserCreate) -> UserEntity:
        try:
            with transaction.atomic():
                user.password = make_password(user.password)
                return self.user_repository.create_user(user)
        except IntegrityError:
            raise UsernameIsNotFreeError(_('Username already exists'))

    def update_user(self, user: UserCreate) -> None:
        try:
            with transaction.atomic():
                user.password = make_password(user.password)
                self.user_repository.update_user(user)
        except IntegrityError:
            raise UsernameIsNotFreeError(_('Username already exists'))

    def delete_user(self, user_id: int) -> None:
        return self.user_repository.delete_user(user_id)

    def get_object(self, user_id: int) -> UserEntity:
        return self.user_repository.get_user(user_id)
