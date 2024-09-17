from dataclasses import dataclass
from datetime import datetime


@dataclass
class StatusOutputEntity:
    id: int  # noqa
    title: str
    created_at: datetime


@dataclass
class StatusInputEntity:
    title: str
