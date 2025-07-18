from pydantic import BaseModel, EmailStr, Field


class RegisterSchema(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    is_term_accepted: bool


class RegisterResponse(BaseModel):
    message: str


class ResendOtpSchema(BaseModel):
    email: EmailStr


class ResendOtpResponse(BaseModel):
    message: str