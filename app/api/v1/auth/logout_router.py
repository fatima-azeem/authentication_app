from fastapi import APIRouter, Depends, Response, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db_session
from app.db.models.session_model import Session

router = APIRouter(prefix="/api/v1", tags=["auth"])


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db_session),
):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        await db.execute(
            Session.__table__.delete().where(Session.refresh_token == refresh_token)
        )
        await db.commit()
    response.delete_cookie("refresh_token")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
