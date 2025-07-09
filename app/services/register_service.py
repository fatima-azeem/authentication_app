from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.register_schema import RegisterSchema, RegisterResponse
from app.db.models.user_model import User
from app.db.models.otp_model import Otp
from app.db.models.enums_model import OtpType
from app.db.models.onboarding_model import OnBoarding
from app.utils.otp_generator import generate_otp
from passlib.hash import argon2
import logging
from app.services.email_service import send_verification_email
from datetime import datetime, timedelta


async def register_user_service(
    payload: RegisterSchema, db: AsyncSession
) -> RegisterResponse:
    # 1. User existence check
    result = await db.execute(select(User).where(User.email == payload.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Terms acceptance check
    if not payload.is_term_accepted:
        raise HTTPException(
            status_code=400, detail="Terms and Conditions must be accepted"
        )

    # 3. Password hashing
    hashed_password = argon2.hash(payload.password)

    # 4. User creation (without full_name)
    user = User(email=payload.email, password=hashed_password)
    db.add(user)
    await db.flush()  # To get user.id

    # 5. OnBoarding record with full_name
    onboarding = OnBoarding(user_id=user.id, full_name=payload.full_name)
    db.add(onboarding)

    # 6. OTP generation and storage (use enum value)
    otp_code = generate_otp()
    otp = Otp(
        user_id=user.id,
        code=otp_code,
        type=OtpType.EMAIL_VERIFICATION,
        expires_at=datetime.utcnow() + timedelta(minutes=10),
    )
    db.add(otp)

    await db.commit()

    # 7. Send verification email
    await send_verification_email(email=payload.email, otp=otp_code)

    # 8. Logging
    logging.info(f"User registered: {user.email}, OTP sent: {otp_code}")

    return RegisterResponse(
        message="Registration successful. Please verify your email."
    )
