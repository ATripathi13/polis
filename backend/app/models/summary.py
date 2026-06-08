import uuid
from sqlalchemy import Text, ForeignKey, UUID, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.organization import TimestampMixin


class Summary(Base, TimestampMixin):
    __tablename__ = "summaries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(Text, default="EXECUTIVE") # BRIEF, DETAILED, EXECUTIVE
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0)
    
    meeting_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("meetings.id"), nullable=False)
    
    # Relationships
    meeting: Mapped["Meeting"] = relationship(back_populates="summaries")
