from django.db import (
    IntegrityError,
    transaction,
)
from django.http import Http404

from task_manager.common.base_service import BaseService
from task_manager.tasks.entities.label_entity import (
    LabelEntity,
    LabelInput,
)
from task_manager.tasks.exceptions.label_exceptions import (
    LabelNameIsNotFreeException,
)
from task_manager.tasks.models import Label
from task_manager.tasks.repositories.label_repository import LabelRepository


class LabelService(BaseService):
    def __init__(self):
        self.repository = LabelRepository()

    def get_all_objects(self) -> list[LabelEntity]:
        return self.repository.get_all_objects()

    def get_object(self, label_id: int) -> LabelEntity:
        try:
            return self.repository.get_object(label_id)
        except Label.DoesNotExist:
            raise Http404

    def create_object(self, label: LabelEntity) -> None:
        try:
            with transaction.atomic():
                self.repository.create_object(label)

        except IntegrityError:
            raise LabelNameIsNotFreeException

    def update_object(self, label_id: int, label: LabelInput) -> None:
        if not self.repository.is_object_name_free(label.name, label_id):
            raise LabelNameIsNotFreeException

        self.repository.update_object(label_id, label)

    def delete_object(self, label_id: int) -> None:
        self.repository.delete_object(label_id)
