from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserEntity:
    id: int  # noqa
    username: str
    full_name: str
    password: str
    created_at: datetime


@dataclass
class UserInput:
    first_name: str
    last_name: str
    username: str
    password: str
