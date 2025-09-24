from sqlalchemy import VARCHAR, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.base import BaseTimeModel


class Comment(BaseTimeModel):
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"), unique=True)
    description: Mapped[str] = mapped_column(VARCHAR(255))

    lead: Mapped["Lead"] = relationship("Lead", back_populates="comment")
