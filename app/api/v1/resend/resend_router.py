from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db_session
from app.schemas.register_schema import ResendOtpSchema
from app.services.resend_service import resend_email_verification_otp, resend_password_reset_otp

router = APIRouter(prefix="/api/v1", tags=["auth"])


@router.post("/resend-email-verification-otp", status_code=status.HTTP_204_NO_CONTENT)
async def resend_email_verification_otp_endpoint(
    payload: ResendOtpSchema,
    db: AsyncSession = Depends(get_db_session),
):
    """Resend email verification OTP"""
    await resend_email_verification_otp(payload.email, db)


@router.post("/resend-password-reset-otp", status_code=status.HTTP_204_NO_CONTENT)
async def resend_password_reset_otp_endpoint(
    payload: ResendOtpSchema,
    db: AsyncSession = Depends(get_db_session),
):
    """Resend password reset OTP"""
    await resend_password_reset_otp(payload.email, db)
