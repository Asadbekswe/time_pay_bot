from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy import VARCHAR
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.base import BaseTimeModel


class Meeting(BaseTimeModel):
    operator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"))

    meeting_date: Mapped[datetime] = mapped_column(DateTime)
    address: Mapped[str] = mapped_column(VARCHAR(255))

    operator: Mapped["User"] = relationship("User", back_populates="meetings")
    lead: Mapped["Lead"] = relationship("Lead", back_populates="meetings")
