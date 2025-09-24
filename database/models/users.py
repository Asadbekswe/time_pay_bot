from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Enum as SQLEnum, INTEGER, ForeignKey, DateTime
from sqlalchemy import VARCHAR
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.base import TimeBasedModel, BaseTimeModel


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


class Comment(BaseTimeModel):
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"), unique=True)
    description: Mapped[str] = mapped_column(VARCHAR(255))

    lead: Mapped["Lead"] = relationship("Lead", back_populates="comment")


class Lead(BaseTimeModel):
    class Status(Enum):
        SOLD = "sold"
        NOT_SOLD = "not_sold"
        CANT_BUY = "cant_buy"
        NEW_LEAD = "new_lead"

    visit_by: Mapped[str] = mapped_column(VARCHAR(100), nullable=True)
    lead_id: Mapped[int] = mapped_column(INTEGER, nullable=True)
    status: Mapped[Status] = mapped_column(SQLEnum(Status), default=Status.NOT_SOLD)
    reminder_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    operator_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="leads", foreign_keys=[user_id])
    operator: Mapped[Optional["User"]] = relationship("User", back_populates="operated_leads",
                                                      foreign_keys=[operator_id])
    comment: Mapped[Optional["Comment"]] = relationship("Comment", back_populates="lead", uselist=False,
                                                        cascade="all, delete-orphan")

    meetings: Mapped[list["Meeting"]] = relationship("Meeting", back_populates="lead")


class Meeting(BaseTimeModel):
    operator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"))

    meeting_date: Mapped[datetime] = mapped_column(DateTime)
    address: Mapped[str] = mapped_column(VARCHAR(255))

    operator: Mapped["User"] = relationship("User", back_populates="meetings")
    lead: Mapped["Lead"] = relationship("Lead", back_populates="meetings")
