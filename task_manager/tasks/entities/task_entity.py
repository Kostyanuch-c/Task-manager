from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime

from django.contrib.auth.models import AbstractUser

from task_manager.tasks.models import (
    Label,
    Status,
)


@dataclass
class TaskEntity:
    id: int  # noqa
    name: str
    description: str | None
    status: Status
    author: AbstractUser
    executor: AbstractUser | None
    labels: Iterable[Label] | None
    created_at: datetime


@dataclass
class TaskInput:
    name: str
    description: str | None
    status: Status
    author: AbstractUser
    executor: AbstractUser | None
    labels: Iterable[Label] | None


@dataclass
class TaskOutputTemplateDetail:
    id: int  # noqa
    name: str
    description: str | None
    status_name: str
    author_full_name: str
    executor_full_name: str | None
    labels: Iterable[Label] | None
    created_at: datetime
