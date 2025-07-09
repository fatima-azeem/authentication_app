from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings
from app.db.models.base_model import Base

# Create the async engine
engine = create_async_engine(
    settings.async_db_uri,
    echo=settings.DB_ECHO,
    future=True,
)

# Create a sessionmaker factory for async sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


# Dependency for FastAPI routes
async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session
