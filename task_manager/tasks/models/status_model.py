from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.common.models import BaseTimedModel
from task_manager.tasks.entities.status_entity import StatusOutputEntity


class Status(BaseTimedModel):
    title = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        unique=True,
    )

    def to_entity(self):
        return StatusOutputEntity(
            id=self.id,
            title=self.title,
            created_at=self.created_at,
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"
