from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db_session
from app.schemas.otp_schema import VerifyOtpSchema, OtpVerifyResponse
from app.services.otp_service import verify_otp_service

router = APIRouter(prefix="/api/v1", tags=["otp"])


@router.post(
    "/verify-otp", status_code=status.HTTP_200_OK, response_model=OtpVerifyResponse
)
async def verify_otp(
    payload: VerifyOtpSchema,
    db: AsyncSession = Depends(get_db_session),
):
    return await verify_otp_service(payload, db)
