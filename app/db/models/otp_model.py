from sqlalchemy import String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base_model import Base
from .enums_model import OtpType
from .user_model import User
from app.utils.generate_cuid import generate_cuid


class Otp(Base):
    __tablename__ = "otp"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_cuid)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    code: Mapped[str] = mapped_column(String)
    type: Mapped[OtpType] = mapped_column(Enum(OtpType))
    expires_at: Mapped[DateTime] = mapped_column(DateTime)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="otps")
