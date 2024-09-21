from dataclasses import dataclass
from datetime import datetime


@dataclass
class StatusEntity:
    id: int  # noqa
    name: str
    created_at: datetime


@dataclass
class StatusInput:
    name: str
