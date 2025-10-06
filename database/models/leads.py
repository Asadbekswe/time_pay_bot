from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Enum as SQLEnum, ForeignKey, DateTime
from sqlalchemy import VARCHAR
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.base import BaseTimeModel


class Lead(BaseTimeModel):
    class Status(Enum):
        NEW = "NEW"
        CONTACTED = "CONTACTED"
        FOLLOW_UP = "FOLLOW_UP"
        INTERESTED = "INTERESTED"
        NOT_INTERESTED = "NOT_INTERESTED"
        CANNOT_AFFORD = "CANNOT_AFFORD"
        SOLD = "SOLD"
        LOST = "LOST"

    visit_by: Mapped[str] = mapped_column(VARCHAR(100), nullable=True)
    status: Mapped[Status] = mapped_column(SQLEnum(Status), default=Status.NEW)

    sold_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    operator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="leads", foreign_keys=[user_id])
    operator: Mapped[Optional["User"]] = relationship("User", back_populates="operated_leads",
                                                      foreign_keys=[operator_id])
    comment: Mapped[Optional["Comment"]] = relationship("Comment", back_populates="lead", uselist=False,
                                                        cascade="all, delete-orphan")

    meetings: Mapped[list["Meeting"]] = relationship("Meeting", back_populates="lead")
