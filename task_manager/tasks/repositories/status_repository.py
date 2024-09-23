from django.db.models import Q
from django.shortcuts import get_object_or_404

from task_manager.common.base_repositories import BaseRepository
from task_manager.tasks.entities.status_entity import (
    StatusEntity,
    StatusInput,
)
from task_manager.tasks.models import Status


class StatusRepository(BaseRepository):
    def __init__(self):
        self.status = Status

    def is_object_name_free(self, name: str, status_id: int) -> bool:
        return not self.status.objects.filter(
            Q(name=name) & ~Q(id=status_id),
        ).exists()

    def get_all_objects(self) -> list[StatusEntity]:
        queryset = self.status.objects.all()
        return [status.to_entity() for status in queryset]

    def create_object(self, status: StatusInput) -> None:
        self.status.objects.create(
            name=status.name,
        )

    def update_object(
            self,
            status_id: int,
            status_data: StatusInput,
    ) -> None:
        self.status.objects.filter(id=status_id).update(
            name=status_data.name,
        )

    def delete_object(self, status_id: int) -> None:
        self.status.objects.filter(id=status_id).delete()

    def get_object(self, status_id: int) -> StatusEntity:
        return get_object_or_404(self.status, id=status_id)
