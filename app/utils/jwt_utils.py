from datetime import datetime, timedelta
from typing import Any, Dict
from jose import jwt, JWTError
from app.core.config import settings

ALGORITHM = "HS256"


def create_access_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_ACCESS_TOKEN_SECRET, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_REFRESH_TOKEN_SECRET, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token, settings.JWT_ACCESS_TOKEN_SECRET, algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        return None  # type: ignore


def decode_refresh_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token, settings.JWT_REFRESH_TOKEN_SECRET, algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        return None  # type: ignore
