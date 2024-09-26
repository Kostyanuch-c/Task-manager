from django.contrib.auth.models import AbstractUser

from task_manager.users.entities import UserEntity as UserEntity


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
            first_name=self.first_name,
            last_name=self.last_name,
            full_name=self.full_name,
        )

    def __str__(self) -> str:
        return self.username

    class Meta:
        ordering = ["id"]
