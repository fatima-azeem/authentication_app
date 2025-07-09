from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db_session
from app.schemas.login_schema import LoginSchema, LoginResponse
from app.services.login_service import login_service

router = APIRouter(prefix="/api/v1", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(
    payload: LoginSchema,
    response: Response,
    request: Request,  # Add request to extract headers and client info
    db: AsyncSession = Depends(get_db_session),
):
    ip_address = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    device_id = payload.device_id or f"{ip_address}-{user_agent[:20]}"
    access_token, refresh_token = await login_service(
        payload, db, device_id=device_id, ip_address=ip_address, user_agent=user_agent
    )
    # Set refresh token as HTTP-only cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        samesite="lax",
        secure=True,
    )
    return LoginResponse(access_token=access_token)
