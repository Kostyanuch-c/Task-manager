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
        "Status",
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
        'Label',
        through='Membership',
        verbose_name=_("Labels"),
        blank=True,
        related_name="task_as_label",

    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class Membership(models.Model):
    label = models.ForeignKey(
        'Label',
        on_delete=models.PROTECT,
        verbose_name=_("Label"),
    )
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        verbose_name=_("Task"),
    )

    class Meta:
        db_table = 'task_label_membership'
        verbose_name = "Membership"
        verbose_name_plural = "Memberships"
