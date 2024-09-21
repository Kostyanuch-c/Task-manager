from dataclasses import dataclass
from datetime import datetime

from task_manager.tasks.models import Status
from task_manager.users.models import User


@dataclass
class TaskEntity:
    id: int  # noqa
    name: str
    description: str | None
    status: Status
    author: User
    executor: User | None
    created_at: datetime


@dataclass
class TaskInput:
    name: str
    description: str | None
    status: Status
    author: User
    executor: User | None


@dataclass
class TaskOutputTemplate:
    id: int  # noqa
    name: str
    description: str | None
    status_name: str
    author_full_name: str
    executor_full_name: str | None
    created_at: datetime
