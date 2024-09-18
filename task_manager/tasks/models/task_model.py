from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.common.models import BaseTimedModel
from task_manager.tasks.entities.task_entity import TaskEntity


class Task(BaseTimedModel):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        unique=True,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        null=True,
    )
    status = models.ForeignKey(
        "Status",
        on_delete=models.PROTECT,
        verbose_name=_("Status"),
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        verbose_name=_("Author"),
        related_name="task_as_author",
    )

    performer = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        verbose_name=_("Performer"),
        blank=True,
        null=True,
        related_name="task_as_performer",
    )

    def to_entity(self):
        return TaskEntity(
            id=self.id,
            name=self.name,
            description=self.description,
            status_name=self.status.title,
            author_full_name=self.author.full_name,
            performer_full_name=self.performer.full_name
            if self.performer
            else None,
            created_at=self.created_at,
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
