from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db_session
from sqlalchemy import text
from app.api.v1.register.register_router import router as register_router
from app.api.v1.otp.otp_router import router as otp_router
from app.api.v1.auth.auth_router import router as auth_router
from app.api.v1.auth.logout_router import router as logout_router
from app.api.v1.auth.password_reset_router import router as password_reset_router
from app.api.v1.resend.resend_router import router as resend_router
from app.core.security import api_key_validator


app = FastAPI()

app.include_router(register_router, dependencies=[Depends(api_key_validator)])
app.include_router(otp_router, dependencies=[Depends(api_key_validator)])
app.include_router(resend_router, dependencies=[Depends(api_key_validator)])
app.include_router(auth_router)
app.include_router(logout_router)
app.include_router(password_reset_router)


@app.get("/health")
async def db_test(session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(text("SELECT 101"))
    return {"db_response": result.scalar_one()}

