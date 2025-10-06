from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Enum as SQLEnum, INTEGER, ForeignKey, DateTime
from sqlalchemy import VARCHAR
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.base import TimeBasedModel, BaseTimeModel


class Lead(BaseTimeModel):
    class Status(Enum):
        SOLD = "sold"
        NOT_SOLD = "not_sold"
        CANT_BUY = "cant_buy"
        NEW_LEAD = "new_lead"

    visit_by: Mapped[str] = mapped_column(VARCHAR(100), nullable=True)
    lead_id: Mapped[int] = mapped_column(INTEGER, nullable=True)
    status: Mapped[Status] = mapped_column(SQLEnum(Status), default=Status.NEW_LEAD)
    reminder_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    solt_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    operator_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="leads", foreign_keys=[user_id])
    operator: Mapped[Optional["User"]] = relationship("User", back_populates="operated_leads",
                                                      foreign_keys=[operator_id])
    comment: Mapped[Optional["Comment"]] = relationship("Comment", back_populates="lead", uselist=False,
                                                        cascade="all, delete-orphan")

    meetings: Mapped[list["Meeting"]] = relationship("Meeting", back_populates="lead")
