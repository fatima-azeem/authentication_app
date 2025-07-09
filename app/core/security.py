from fastapi import Header, HTTPException, status
from app.core.config import settings

def api_key_validator(x_api_key: str = Header(...)):
    if not x_api_key or x_api_key != settings.BACKEND_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
