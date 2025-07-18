from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.user_model import User
from app.db.models.otp_model import Otp
from app.db.models.enums_model import OtpType
from app.db.models.password_reset_token import PasswordResetToken
from app.utils.otp_generator import generate_otp
from app.services.email_service import send_verification_email
from datetime import datetime, timedelta
import logging


async def resend_email_verification_otp(email: str, db: AsyncSession):
    """Resend email verification OTP"""
    # Check if user exists
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Check if user is already verified
    if user.is_email_verified:
        raise HTTPException(status_code=400, detail="Email already verified")
    
    # Delete existing OTP for this user
    await db.execute(
        Otp.__table__.delete().where(
            Otp.user_id == user.id,
            Otp.type == OtpType.EMAIL_VERIFICATION
        )
    )
    
    # Generate new OTP
    otp_code = generate_otp()
    otp = Otp(
        user_id=user.id,
        code=otp_code,
        type=OtpType.EMAIL_VERIFICATION,
        expires_at=datetime.utcnow() + timedelta(minutes=10),
    )
    db.add(otp)
    await db.commit()
    
    # Send verification email
    await send_verification_email(email=email, otp=otp_code)
    
    logging.info(f"OTP resent to {email}: {otp_code}")


async def resend_password_reset_otp(email: str, db: AsyncSession):
    """Resend password reset OTP"""
    # Check if user exists
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        # Don't reveal if user exists for security
        return
    
    # Delete existing password reset tokens for this user
    await db.execute(
        PasswordResetToken.__table__.delete().where(
            PasswordResetToken.user_id == user.id
        )
    )
    
    # Generate new token
    import secrets
    otp = f"{secrets.randbelow(1000000):06d}"
    expires_at = datetime.utcnow() + timedelta(hours=1)
    
    reset_token = PasswordResetToken(
        user_id=user.id,
        token=otp,
        expires_at=expires_at
    )
    db.add(reset_token)
    await db.commit()
    
    # Send password reset email
    await send_verification_email(email=email, otp=otp)
    
    logging.info(f"Password reset OTP resent to {email}: {otp}")
