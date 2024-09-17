from django.shortcuts import get_object_or_404

from task_manager.common.base_repositories import BaseRepository
from task_manager.tasks.entities.status_entity import (
    StatusInputEntity,
    StatusOutputEntity,
)
from task_manager.tasks.models import Status


class StatusRepository(BaseRepository):
    def __init__(self):
        self.status = Status

    def is_object_name_free(self, title: str) -> bool:
        return not self.status.objects.filter(title=title).exists()

    def get_all_objects(self) -> list[StatusOutputEntity]:
        queryset = self.status.objects.all()
        return [status.to_entity() for status in queryset]

    def create_object(self, status: StatusInputEntity) -> StatusOutputEntity:
        queryset = self.status.objects.create(
            title=status.title,
        )
        return queryset.to_entity()

    def update_object(
        self, status_id: int, status_data: StatusInputEntity,
    ) -> None:
        self.status.objects.filter(id=status_id).update(
            title=status_data.title,
        )

    def delete_object(self, status_id: int) -> None:
        self.status.objects.filter(id=status_id).delete()

    def get_object(self, status_id: int) -> StatusOutputEntity:
        return get_object_or_404(self.status, id=status_id)
