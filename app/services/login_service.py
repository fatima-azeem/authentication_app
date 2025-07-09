from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.hash import argon2
from datetime import datetime, timedelta

from app.db.models.user_model import User
from app.db.models.session_model import Session
from app.utils.jwt_utils import create_access_token, create_refresh_token
from app.schemas.login_schema import LoginSchema


async def login_service(
    payload: LoginSchema,
    db: AsyncSession,
    device_id: str,
    ip_address: str,
    user_agent: str,
):
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if not user or not argon2.verify(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.id})
    refresh_token = create_refresh_token({"sub": user.id})

    # Save session
    expires_at = datetime.utcnow() + timedelta(days=7)
    session = Session(
        user_id=user.id,
        refresh_token=refresh_token,
        expires_at=expires_at,
        device_id=device_id,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    db.add(session)
    await db.commit()

    return access_token, refresh_token
