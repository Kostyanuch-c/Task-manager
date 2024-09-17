from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserOutputEntity:
    id: int  # noqa
    username: str
    full_name: str
    password: str
    created_at: datetime


@dataclass
class UserInputEntity:
    first_name: str
    last_name: str
    username: str
    password: str
