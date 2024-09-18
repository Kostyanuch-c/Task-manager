from dataclasses import dataclass
from datetime import datetime


@dataclass
class StatusEntity:
    id: int  # noqa
    title: str
    created_at: datetime


@dataclass
class StatusInput:
    title: str
