from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int  # noqa
    first_name: str
    last_name: str
    username: str
    password: str
    date_joined: datetime


@dataclass
class UserCreate:
    first_name: str
    last_name: str
    username: str
    password: str
