from sqlalchemy import String, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base_model import Base
from .enums_model import UserRole, OtpPurpose
from typing import Optional, List, TYPE_CHECKING
from app.utils.generate_cuid import generate_cuid


if TYPE_CHECKING:
    from .onboarding_model import OnBoarding
    from .session_model import Session
    from .otp_model import Otp


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_cuid)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_term_accepted: Mapped[bool] = mapped_column(Boolean, default=False)
    otp_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    otp_purpose: Mapped[Optional[OtpPurpose]] = mapped_column(
        Enum(OtpPurpose), nullable=True
    )
    otp_expires_at: Mapped[Optional[DateTime]] = mapped_column(DateTime, nullable=True)
    refresh_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    on_boarding: Mapped[Optional["OnBoarding"]] = relationship(
        "OnBoarding", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    sessions: Mapped[List["Session"]] = relationship(
        "Session", back_populates="user", cascade="all, delete-orphan"
    )
    otps: Mapped[List["Otp"]] = relationship(
        "Otp", back_populates="user", cascade="all, delete-orphan"
    )
