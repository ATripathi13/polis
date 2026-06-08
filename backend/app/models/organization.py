import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from app.database import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Organization(Base, TimestampMixin):
    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    # Relationships
    users: Mapped[List["User"]] = relationship(back_populates="organization", cascade="all, delete-orphan")
    meetings: Mapped[List["Meeting"]] = relationship(back_populates="organization", cascade="all, delete-orphan")
    documents: Mapped[List["Document"]] = relationship(back_populates="organization", cascade="all, delete-orphan")
