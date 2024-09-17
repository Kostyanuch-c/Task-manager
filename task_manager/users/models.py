from django.contrib.auth.models import AbstractUser

from task_manager.users.entities import UserOutputEntity as UserEntity


class User(AbstractUser):
    @property
    def full_name(self):
        """Returns the user full name."""
        return f"{self.first_name} {self.last_name}"

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            username=self.username,
            password=self.password,
            created_at=self.date_joined,
            full_name=self.full_name,
        )

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
