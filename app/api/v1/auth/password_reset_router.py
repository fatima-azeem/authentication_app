from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db_session
from app.schemas.password_reset_schema import (
    PasswordResetRequestSchema,
    PasswordResetSchema,
    PasswordResetResponse,
)
from app.services.password_reset_service import request_password_reset, reset_password

router = APIRouter(prefix="/api/v1", tags=["auth"])


@router.post("/request-password-reset", status_code=status.HTTP_204_NO_CONTENT)
async def request_password_reset_endpoint(
    payload: PasswordResetRequestSchema,
    db: AsyncSession = Depends(get_db_session),
):
    await request_password_reset(payload.email, db)
    return 


@router.post("/reset-password", response_model=PasswordResetResponse)
async def reset_password_endpoint(
    payload: PasswordResetSchema,
    db: AsyncSession = Depends(get_db_session),
):
    if len(payload.new_password) < 8:
        return PasswordResetResponse(message="Password must be at least 8 characters.")
    await reset_password(payload.token, payload.new_password, db)
    return PasswordResetResponse(message="Password reset successful.")
