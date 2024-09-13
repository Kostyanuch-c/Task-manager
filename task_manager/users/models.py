from django.contrib.auth.models import AbstractUser

from task_manager.users.entities import User as UserEntity


class User(AbstractUser):

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
            password=self.password,
            date_joined=self.date_joined,
        )

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
