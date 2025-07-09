from typing import Optional
from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    device_id: Optional[str] = None  # Optional, fallback if not provided


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
