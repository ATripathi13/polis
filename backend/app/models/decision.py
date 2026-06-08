import uuid
from sqlalchemy import Text, ForeignKey, UUID, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.database import Base
from app.models.organization import TimestampMixin


class Decision(Base, TimestampMixin):
    __tablename__ = "decisions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    rationale: Mapped[Optional[str]] = mapped_column(Text)
    approver: Mapped[Optional[str]] = mapped_column(Text)
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0)
    
    meeting_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("meetings.id"), nullable=False)
    
    # Relationships
    meeting: Mapped["Meeting"] = relationship(back_populates="decisions")
