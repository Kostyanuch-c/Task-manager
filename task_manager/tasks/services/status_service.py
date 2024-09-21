from django.db import (
    IntegrityError,
    transaction,
)
from django.db.models import ProtectedError

from task_manager.common.base_service import BaseService
from task_manager.tasks.entities.status_entity import (
    StatusEntity,
    StatusInput,
)
from task_manager.tasks.exceptions.status_exceptions import (
    StatusDeleteProtectedError,
    StatusTitleIsNotFreeException,
)
from task_manager.tasks.repositories.status_repository import StatusRepository


class StatusService(BaseService):
    def __init__(self):
        self.repository = StatusRepository()

    def get_all_objects(self) -> list[StatusEntity]:
        return self.repository.get_all_objects()

    def get_object(self, status_id: int) -> StatusEntity:
        return self.repository.get_object(status_id)

    def create_object(self, status: StatusInput) -> None:
        try:
            with transaction.atomic():
                return self.repository.create_object(status=status)

        except IntegrityError:
            raise StatusTitleIsNotFreeException()

    def update_object(
        self,
        status_id: int,
        status: StatusInput,
    ) -> None:
        if not self.repository.is_object_name_free(status.name):
            raise StatusTitleIsNotFreeException()

        self.repository.update_object(status_id, status)

    def delete_object(self, status_id: int) -> None:
        try:
            return self.repository.delete_object(status_id)
        except ProtectedError:
            raise StatusDeleteProtectedError
