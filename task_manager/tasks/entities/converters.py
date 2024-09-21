from task_manager.tasks.entities.task_entity import (
    TaskEntity,
    TaskOutputTemplate,
)


class TaskEntityConverter:
    @staticmethod
    def to_output_template(entity: TaskEntity) -> TaskOutputTemplate:
        return TaskOutputTemplate(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            status_name=entity.status.name,
            author_full_name=entity.author.full_name,
            executor_full_name=entity.executor.full_name
            if entity.executor
            else None,
            created_at=entity.created_at,
        )

    @staticmethod
    def to_output_list(entities: list[TaskEntity]) -> list[TaskOutputTemplate]:
        return [
            TaskEntityConverter.to_output_template(entity)
            for entity in entities
        ]
