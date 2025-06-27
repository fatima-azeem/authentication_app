from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db_session
from sqlalchemy import text

router = FastAPI()

@router.get("/db-test")
async def db_test(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(text("SELECT 1"))
    return {"success": result.scalar() == 1}