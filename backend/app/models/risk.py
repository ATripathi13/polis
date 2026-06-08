import uuid
from sqlalchemy import String, Text, ForeignKey, UUID, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.organization import TimestampMixin


class Risk(Base, TimestampMixin):
    __tablename__ = "risks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category: Mapped[str] = mapped_column(String(100), nullable=False) # Technical, Operational, etc.
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="MEDIUM")
    likelihood: Mapped[str] = mapped_column(String(50), default="MEDIUM")
    impact: Mapped[str] = mapped_column(String(50), default="MEDIUM")
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0)
    
    meeting_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("meetings.id"), nullable=False)
    
    # Relationships
    meeting: Mapped["Meeting"] = relationship(back_populates="risks")
