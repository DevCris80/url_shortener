import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from db.base import Base
from db.model_url import URL
from core.config import settings

async def init_db():
    engine = create_async_engine(settings.db_url, echo=True)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    await engine.dispose()
    print("Database initialized successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())
