import enum

from sqlalchemy import Enum


class Role(enum.Enum):
    administrator: str = "administrator"
    moderator: str = "moderator"
    user: str = "user"

