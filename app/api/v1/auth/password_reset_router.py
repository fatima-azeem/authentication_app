from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from app.db.database import get_db_session
from app.schemas.password_reset_schema import (
    PasswordResetRequestSchema,
    PasswordResetSchema,
    PasswordResetResponse,
)
from app.schemas.otp_schema import VerifyOtpSchema, OtpVerifyResponse
from app.services.password_reset_service import request_password_reset, reset_password
from app.db.models.password_reset_token import PasswordResetToken

router = APIRouter(prefix="/api/v1", tags=["auth"])


@router.post("/request-password-reset", status_code=status.HTTP_204_NO_CONTENT)
async def request_password_reset_endpoint(
    payload: PasswordResetRequestSchema,
    db: AsyncSession = Depends(get_db_session),
):
    await request_password_reset(payload.email, db)
    return 


@router.post("/verify-password-reset-otp", response_model=OtpVerifyResponse)
async def verify_password_reset_otp(
    payload: VerifyOtpSchema,
    db: AsyncSession = Depends(get_db_session),
):
    """Verify OTP for password reset"""
    result = await db.execute(
        select(PasswordResetToken).where(
            PasswordResetToken.token == payload.otp
        ).order_by(PasswordResetToken.created_at.desc())
    )
    reset_token = result.scalar_one_or_none()
    
    if not reset_token:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    if reset_token.used:
        raise HTTPException(status_code=400, detail="OTP already used")
    
    if reset_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")
    
    # Don't mark as used yet - we'll do that when password is actually reset
    return OtpVerifyResponse(message="OTP verified successfully. You can now reset your password.")


@router.post("/reset-password", response_model=PasswordResetResponse)
async def reset_password_endpoint(
    payload: PasswordResetSchema,
    db: AsyncSession = Depends(get_db_session),
):
    if len(payload.new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters.")
    await reset_password(payload.token, payload.new_password, db)
    return PasswordResetResponse(message="Password reset successful.")
