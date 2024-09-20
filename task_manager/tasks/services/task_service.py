from django.db import (
    IntegrityError,
    transaction,
)
from django.http import Http404

from task_manager.common.base_service import BaseService
from task_manager.tasks.entities.task_entity import (
    TaskEntity,
    TaskInput,
)
from task_manager.tasks.exceptions.task_exceptions import (
    TaskNameIsNotFreeException,
)
from task_manager.tasks.models import Task
from task_manager.tasks.repositories.task_repository import TaskRepository
from task_manager.users.models import User


class TaskService(BaseService):
    def __init__(self):
        self.repository = TaskRepository()

    def get_all_objects(self) -> list[TaskEntity]:
        return self.repository.get_all_objects()

    def get_object(self, task_id: int) -> TaskEntity:
        try:
            return self.repository.get_object(task_id)
        except Task.DoesNotExist:
            raise Http404

    def create_object(self, task: TaskInput) -> TaskEntity:
        try:
            with transaction.atomic():
                return self.repository.create_object(task)

        except IntegrityError:
            raise TaskNameIsNotFreeException

    def update_object(self, task_id: int, task: TaskInput) -> None:
        if not self.repository.is_object_name_free(task.name):
            raise TaskNameIsNotFreeException

        self.repository.update_object(task_id, task)

    def delete_object(self, task_id: int) -> None:
        self.repository.delete_object(task_id)

    @staticmethod
    def check_permissions(request_user: User, task: TaskEntity) -> bool:
        return request_user == task.author
