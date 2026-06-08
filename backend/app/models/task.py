import uuid
from sqlalchemy import String, Text, ForeignKey, UUID, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.database import Base
from app.models.organization import TimestampMixin


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    owner: Mapped[Optional[str]] = mapped_column(String(255))
    deadline: Mapped[Optional[str]] = mapped_column(String(100)) # Can be fuzzy like "tomorrow" or date
    priority: Mapped[str] = mapped_column(String(50), default="MEDIUM") # LOW, MEDIUM, HIGH, CRITICAL
    status: Mapped[str] = mapped_column(String(50), default="OPEN")
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0)
    
    meeting_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("meetings.id"), nullable=False)
    
    # Relationships
    meeting: Mapped["Meeting"] = relationship(back_populates="tasks")


class Decision(Base, TimestampMixin):
    __tablename__ = "decisions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    rationale: Mapped[Optional[str]] = mapped_column(Text)
    approver: Mapped[Optional[str]] = mapped_column(String(255))
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0)
    
    meeting_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("meetings.id"), nullable=False)
    
    # Relationships
    meeting: Mapped["Meeting"] = relationship(back_populates="decisions")
