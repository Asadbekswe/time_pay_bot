from datetime import datetime, time

from sqlalchemy import VARCHAR, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.base import BaseTimeModel
from sqlalchemy import Time



class Comment(BaseTimeModel):
    description: Mapped[str] = mapped_column(VARCHAR(255))
    reminder_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    reminder_time: Mapped[time] = mapped_column(Time, nullable=True)

    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"))
    lead: Mapped["Lead"] = relationship("Lead", back_populates="comment")