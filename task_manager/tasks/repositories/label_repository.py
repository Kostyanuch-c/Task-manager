from django.db.models import Q

from task_manager.common.base_repositories import BaseRepository
from task_manager.tasks.entities.label_entity import (
    LabelEntity,
    LabelInput,
)
from task_manager.tasks.models import Label


class LabelRepository(BaseRepository):
    def __init__(self):
        self.label = Label

    def is_object_name_free(self, name: str, label_id: int) -> bool:
        return not self.label.objects.filter(
            Q(name=name) & ~Q(id=label_id),
        ).exists()

    def get_all_objects(self) -> list[LabelEntity]:
        queryset = self.label.objects.all()
        return [label.to_entity() for label in queryset]

    def get_object(self, label_id: int) -> LabelEntity:
        return self.label.objects.get(id=label_id).to_entity()

    def create_object(self, label: LabelInput) -> None:
        self.label.objects.create(name=label.name)

    def update_object(self, label_id: int, label: LabelInput) -> None:
        self.label.objects.filter(id=label_id).update(name=label.name)

    def delete_object(self, label_id: int) -> None:
        self.label.objects.filter(id=label_id).delete()
