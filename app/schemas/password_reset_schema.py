from pydantic import BaseModel, EmailStr


class PasswordResetRequestSchema(BaseModel):
    email: EmailStr


class PasswordResetSchema(BaseModel):
    token: str
    new_password: str  # min_length will be validated in endpoint


class PasswordResetResponse(BaseModel):
    message: str
