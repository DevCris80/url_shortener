from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import random

from db.model_url import URL
from schemas.url import URLCreate


class Shortener:
    CHARACTERS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    SHORT_URL_LENGTH = 6

    async def _long_url_exists(self, db: AsyncSession, long_url: str) -> URL:
        result = await db.execute(select(URL).where(URL.long_url == str(long_url)))
        return result.scalar_one_or_none()

    async def _short_url_exists(self, db: AsyncSession, short_url: str) -> URL:
        result = await db.execute(select(URL).where(URL.short_url == str(short_url)))
        return result.scalar_one_or_none()

    async def short_url(self, db: AsyncSession, url_create: URLCreate) -> URL:
        existing_url = await self._long_url_exists(db, str(url_create.long_url))
        if existing_url:
            return existing_url

        for _ in range(10): 
            short_url = ''.join(random.choices(self.CHARACTERS, k=self.SHORT_URL_LENGTH))
            if not await self._short_url_exists(db, short_url):
                new_url = URL(long_url=str(url_create.long_url), short_url=short_url, user_id=url_create.user_id)
                db.add(new_url)
                await db.commit()
                await db.refresh(new_url)
                return new_url
        raise ValueError("Could not generate unique short URL")
    
    async def get_original_url(self, db: AsyncSession, short_url: str) -> str:
        result = await db.execute(select(URL).where(URL.short_url == short_url))
        url_obj = result.scalar_one_or_none()
        if not url_obj:
            raise ValueError("Short URL not found")
        url_obj.clicks += 1
        await db.commit()
        return url_obj.long_url
    
    async def get_clicks(self, db: AsyncSession, short_url: str) -> int:
        result = await db.execute(select(URL).where(URL.short_url == short_url))
        url_obj = result.scalar_one_or_none()
        if not url_obj:
            raise ValueError("Short URL not found")
        return url_obj.clicks
    
    async def list_urls(self, db: AsyncSession) -> list[URL]:
        result = await db.execute(select(URL).limit(10))
        return result.scalars().all()
