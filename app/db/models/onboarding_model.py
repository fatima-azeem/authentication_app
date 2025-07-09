from sqlalchemy import String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base_model import Base
from typing import Optional, TYPE_CHECKING
from app.utils.generate_cuid import generate_cuid

if TYPE_CHECKING:
    from .user_model import User

class OnBoarding(Base):
    __tablename__ = "on_boarding"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_cuid)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), unique=True
    )
    full_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    recovery_email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    whats_app: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    zip_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    linked_in: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    preferred_payment_method: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )
    preferred_theme: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    avatar_image_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship("User", back_populates="on_boarding")
