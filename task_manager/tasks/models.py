from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager import settings
from task_manager.common.models import BaseTimedModel


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
        "statuses.Status",
        on_delete=models.PROTECT,
        verbose_name=_("Status"),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_("Author"),
        related_name="task_as_author",
    )

    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_("Performer"),
        blank=True,
        null=True,
        related_name="task_as_performer",
    )

    labels = models.ManyToManyField(
        "labels.Label",
        through="TaskLabels",
        verbose_name=_("Labels"),
        blank=True,
        related_name="task_as_label",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class TaskLabels(models.Model):
    label = models.ForeignKey(
        "labels.Label",
        on_delete=models.PROTECT,
        verbose_name=_("Label"),
    )
    task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        verbose_name=_("Task"),
    )

    class Meta:
        db_table = "task_label_membership"
        verbose_name = "task_label_membership"
        verbose_name_plural = "task_label_memberships"
