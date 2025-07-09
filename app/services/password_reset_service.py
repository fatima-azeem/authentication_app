import secrets
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.db.models.user_model import User
from app.db.models.password_reset_token import PasswordResetToken
from app.services.email_service import send_verification_email

RESET_TOKEN_EXPIRY_HOURS = 1


async def request_password_reset(email: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        # Don't reveal if user exists
        return
    otp = f"{secrets.randbelow(1000000):06d}"
    expires_at = datetime.utcnow() + timedelta(hours=RESET_TOKEN_EXPIRY_HOURS)
    reset_token = PasswordResetToken(user_id=user.id, token=otp, expires_at=expires_at)
    db.add(reset_token)
    await db.commit()
    await send_verification_email(user.email, otp)


async def reset_password(token: str, new_password: str, db: AsyncSession):
    result = await db.execute(
        select(PasswordResetToken).where(PasswordResetToken.token == token)
    )
    reset_token = result.scalar_one_or_none()
    if (
        not reset_token
        or reset_token.used
        or reset_token.expires_at < datetime.utcnow()
    ):
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user_result = await db.execute(select(User).where(User.id == reset_token.user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    from passlib.hash import argon2

    user.password = argon2.hash(new_password)
    reset_token.used = True
    await db.commit()
