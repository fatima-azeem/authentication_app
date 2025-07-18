from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base_model import Base
from .user_model import User
from app.utils.generate_cuid import generate_cuid


class Session(Base):
    __tablename__ = "session"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_cuid)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    refresh_token: Mapped[str] = mapped_column(Text)
    expires_at: Mapped[DateTime] = mapped_column(DateTime)
    device_id: Mapped[str] = mapped_column(String)
    ip_address: Mapped[str] = mapped_column(String)
    user_agent: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_active: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship("User", back_populates="sessions")

    __table_args__ = (
        Index("ix_session_user_id", "user_id"),
        Index("ix_session_device_id", "device_id"),
        Index("ix_session_refresh_token", "refresh_token"),
    )
