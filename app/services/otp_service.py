from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from app.db.models.user_model import User
from app.db.models.otp_model import Otp
from app.db.models.enums_model import OtpType
from app.schemas.otp_schema import VerifyOtpSchema, OtpVerifyResponse


async def verify_otp_service(
    payload: VerifyOtpSchema, db: AsyncSession
) -> OtpVerifyResponse:
    # 1. Get user
    user_result = await db.execute(select(User).where(User.email == payload.email))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Get OTP (latest, correct type)
    otp_result = await db.execute(
        select(Otp)
        .where(
            Otp.user_id == user.id,
            Otp.code == payload.otp,
            Otp.type == OtpType.EMAIL_VERIFICATION,
        )
        .order_by(Otp.created_at.desc())
    )
    otp = otp_result.scalar_one_or_none()
    if not otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    expires_at = otp.expires_at
    # Convert SQLAlchemy DateTime to Python datetime if needed
    if not isinstance(expires_at, datetime):
        expires_at = datetime.fromisoformat(str(expires_at))
    # Ensure expires_at is a Python datetime object and naive
    if hasattr(expires_at, "tzinfo") and expires_at.tzinfo is not None:
        expires_at = expires_at.astimezone(tz=None).replace(tzinfo=None)
    if expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")

    # 3. Mark user as verified
    user.is_email_verified = True
    # Delete the OTP after successful verification
    await db.delete(otp)
    await db.commit()
    return OtpVerifyResponse(message="Email verified successfully.")
