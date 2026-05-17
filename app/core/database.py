from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


def _build_url(url: str) -> str:
    """Asegura el driver correcto para asyncpg."""
    return (
        url
        .replace("postgresql://", "postgresql+asyncpg://")
        .replace("postgres://", "postgresql+asyncpg://")
        .split("?")[0]  # asyncpg no usa query params de URL
    )


engine = create_async_engine(
    _build_url(settings.DATABASE_URL),
    connect_args={"ssl": "require"},  # Neon exige TLS
    pool_size=5,        # free tier: máx ~10 conexiones totales
    max_overflow=5,     # picos: hasta 10 conexiones simultáneas
    pool_timeout=30,    # segundos esperando una conexión libre
    pool_recycle=300,   # recicla conexiones cada 5 minutos para evitar timeouts
    pool_pre_ping=True, # detecta conexiones muertas antes de usarlas
    echo=settings.DEBUG,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autoflush=False, 
    autocommit=False, 
)


class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()