from django.db import (
    IntegrityError,
    transaction,
)

from task_manager.common.base_service import BaseService
from task_manager.tasks.entities.status_entity import (
    StatusInputEntity,
    StatusOutputEntity,
)
from task_manager.tasks.exceptions.status_exceptions import (
    StatusTitleIsNotFreeException,
)
from task_manager.tasks.repositories.status_repository import StatusRepository


class StatusService(BaseService):
    def __init__(self):
        self.repository = StatusRepository()

    def get_all_objects(self) -> list[StatusOutputEntity]:
        return self.repository.get_all_objects()

    def get_object(self, status_id: int) -> StatusOutputEntity:
        return self.repository.get_object(status_id)

    def create_object(self, status: StatusInputEntity) -> StatusOutputEntity:
        try:
            with transaction.atomic():
                return self.repository.create_object(status=status)

        except IntegrityError:
            raise StatusTitleIsNotFreeException()

    def update_object(
        self,
        status_id: int,
        status: StatusInputEntity,
    ) -> None:
        if not self.repository.is_object_name_free(status.title):
            raise StatusTitleIsNotFreeException()

        self.repository.update_object(status_id, status)

    def delete_object(self, status_id: int) -> None:
        return self.repository.delete_object(status_id)
