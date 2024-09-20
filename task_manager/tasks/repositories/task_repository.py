from django.db.models import Q

from task_manager.common.base_repositories import BaseRepository
from task_manager.tasks.entities.task_entity import (
    TaskEntity,
    TaskInput,
)
from task_manager.tasks.models import Task


class TaskRepository(BaseRepository):
    def __init__(self):
        self.task = Task

    def is_object_name_free(self, name: str) -> bool:
        return not self.task.objects.filter(name=name).exists()

    def get_all_objects(self, query=Q()) -> list[TaskEntity]:
        queryset = self.task.objects.filter(query).select_related(
            "status",
            "author",
            "performer",
        )
        return [task.to_entity() for task in queryset]

    def create_object(self, task: TaskInput) -> TaskEntity:
        queryset = self.task.objects.create(
            name=task.name,
            description=task.description,
            status=task.status,
            author=task.author,
            performer=task.performer,
        )
        return queryset.to_entity()

    def update_object(self, task_id: int, task: TaskInput) -> None:
        self.task.objects.filter(id=task_id).update(
            name=task.name,
            description=task.description,
            status=task.status,
            author=task.author,
            performer=task.performer,
        )

    def delete_object(self, task_id: int) -> None:
        self.task.objects.filter(id=task_id).delete()

    def get_object(self, task_id: int) -> TaskEntity:
        return (
            self.task.objects.filter(id=task_id)
            .select_related("author", "performer")
            .get()
            .to_entity()
        )
