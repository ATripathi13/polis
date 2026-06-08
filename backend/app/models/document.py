import uuid
from sqlalchemy import String, ForeignKey, UUID, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.database import Base
from app.models.organization import TimestampMixin


class Document(Base, TimestampMixin):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50)) # pdf, docx, audio, etc.
    file_size: Mapped[int] = mapped_column(BigInteger)
    
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    meeting_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("meetings.id"))
    
    # Relationships
    organization: Mapped["Organization"] = relationship(back_populates="documents")
    meeting: Mapped[Optional["Meeting"]] = relationship(back_populates="documents")
