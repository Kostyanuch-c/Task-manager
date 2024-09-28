from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.common.models import BaseTimedModel


class Status(BaseTimedModel):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"
