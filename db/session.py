from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import async_sessionmaker

from core.config import settings

engine = create_async_engine(settings.db_url, echo = True)
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()