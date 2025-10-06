from enum import Enum
from typing import Optional

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import VARCHAR
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.base import TimeBasedModel


class User(TimeBasedModel):
    class Type(Enum):
        USER = "user"
        OPERATOR = "operator"
        ADMIN = "admin"
        SUPER_USER = "super_user"

    first_name: Mapped[str] = mapped_column(VARCHAR(100), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(VARCHAR(100), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(VARCHAR(25), nullable=True)
    username: Mapped[Optional[str]] = mapped_column(VARCHAR(100), nullable=True)
    type: Mapped[Type] = mapped_column(SQLEnum(Type), default=Type.USER)
    meetings: Mapped[list["Meeting"]] = relationship("Meeting", back_populates="operator")
    leads: Mapped[list["Lead"]] = relationship("Lead", back_populates="user", foreign_keys="Lead.user_id")
    operated_leads: Mapped[list["Lead"]] = relationship("Lead", back_populates="operator",
                                                        foreign_keys="Lead.operator_id")
