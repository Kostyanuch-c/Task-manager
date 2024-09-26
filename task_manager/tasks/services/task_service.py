from django.db import (
    IntegrityError,
    transaction,
)
from django.db.models import Q
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

    def _get_query(self, query_params: dict, user_id: int) -> Q:
        query = Q()

        user_task = query_params.get("self_tasks")
        if user_task:
            query &= Q(author_id=user_id)

        status_id = query_params.get("status")
        if status_id:
            query &= Q(status_id=status_id)

        executor_id = query_params.get("executor")
        if executor_id:
            query &= Q(executor_id=executor_id)

        label_id = query_params.get('label')
        if label_id:
            query &= Q(labels__id=label_id)

        return query

    def get_all_objects(
            self, query_params=None, user_id=None,
    ) -> list[TaskEntity]:

        if not query_params:
            return self.repository.get_all_objects()

        query = self._get_query(query_params, user_id)
        return self.repository.get_all_objects(query=query)

    def get_object(self, task_id: int) -> TaskEntity:
        try:
            return self.repository.get_object(task_id)
        except Task.DoesNotExist:
            raise Http404

    def create_object(self, task: TaskInput) -> None:
        try:
            with transaction.atomic():
                return self.repository.create_object(task)

        except IntegrityError:
            raise TaskNameIsNotFreeException

    def update_object(self, task_id: int, task: TaskInput) -> None:
        if not self.repository.is_object_name_free(task.name, task_id):
            raise TaskNameIsNotFreeException

        self.repository.update_object(task_id, task)

    def delete_object(self, task_id: int) -> None:
        self.repository.delete_object(task_id)

    @staticmethod
    def check_permissions(request_user: User, task: TaskEntity) -> bool:
        return request_user == task.author
