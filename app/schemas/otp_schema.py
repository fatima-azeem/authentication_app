from pydantic import BaseModel, EmailStr


class VerifyOtpSchema(BaseModel):
    email: EmailStr
    otp: str


class OtpVerifyResponse(BaseModel):
    message: str