from dataclasses import dataclass
from datetime import datetime


@dataclass()
class LabelEntity:
    id: int  # noqa
    name: str
    created_at: datetime


@dataclass()
class LabelInput:
    name: str
