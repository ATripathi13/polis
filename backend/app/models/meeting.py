import uuid
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, UUID, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

from app.database import Base
from app.models.organization import TimestampMixin


class Meeting(Base, TimestampMixin):
    __tablename__ = "meetings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    source: Mapped[str] = mapped_column(String(50))  # zoom, gmeet, recording, manual
    raw_transcript: Mapped[Optional[str]] = mapped_column(Text)
    processed_transcript: Mapped[Optional[str]] = mapped_column(Text)
    speaker_mapping: Mapped[Optional[dict]] = mapped_column(JSON) # Map of speaker IDs to names
    
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    
    # Relationships
    organization: Mapped["Organization"] = relationship(back_populates="meetings")
    tasks: Mapped[List["Task"]] = relationship(back_populates="meeting")
    decisions: Mapped[List["Decision"]] = relationship(back_populates="meeting")
    contradictions: Mapped[List["Contradiction"]] = relationship(back_populates="meeting")
    risks: Mapped[List["Risk"]] = relationship(back_populates="meeting")
    summaries: Mapped[List["Summary"]] = relationship(back_populates="meeting")
    documents: Mapped[List["Document"]] = relationship(back_populates="meeting")
