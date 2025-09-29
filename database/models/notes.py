from datetime import datetime

from sqlalchemy import VARCHAR, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.base import BaseTimeModel


class Note(BaseTimeModel):
    description: Mapped[str] = mapped_column(VARCHAR(255))
    note_time: Mapped[datetime] = mapped_column(DateTime)

    operator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="notes")
