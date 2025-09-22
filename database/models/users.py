from enum import Enum
from typing import Optional

from sqlalchemy import Enum as SQLEnum, INTEGER
from sqlalchemy import VARCHAR
from sqlalchemy.orm import mapped_column, Mapped

from database.base import TimeBasedModel


class User(TimeBasedModel):
    class Type(Enum):
        USER = "USER"
        OPERATOR = "OPERATOR"
        ADMIN = "ADMIN"
        SUPER_USER = "SUPER_USER"

    first_name: Mapped[str] = mapped_column(VARCHAR(100), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(VARCHAR(100), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(VARCHAR(25), nullable=True)
    username: Mapped[Optional[str]] = mapped_column(VARCHAR(100), nullable=True)
    type: Mapped[Type] = mapped_column(SQLEnum(Type), default=Type.USER)


class Lid(TimeBasedModel):
    visit_by: Mapped[str] = mapped_column(VARCHAR(100), nullable=True)
    lid_id: Mapped[int] = mapped_column(INTEGER, nullable=True)
