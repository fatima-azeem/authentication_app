from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session
from app.schemas.register_schema import RegisterSchema, RegisterResponse
from app.services.register_service import register_user_service

router = APIRouter(prefix="/api/v1", tags=["auth"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterResponse,
)
async def register_user(
    payload: RegisterSchema,
    db: AsyncSession = Depends(get_db_session),
):
    """
    User registration endpoint.
    Expects JSON body and x-api-key header.
    """
    return await register_user_service(payload, db)
