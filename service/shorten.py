from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import random

from db.model_url import URL


class Shortener:
    CHARACTERS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    SHORT_URL_LENGTH = 6

    async def _url_exists(self, db: AsyncSession, long_url: str) -> bool:
        result = await db.execute(select(URL).where(URL.long_url == str(long_url)))
        return result.scalar() is not None

    async def short_url(self, db: AsyncSession, long_url: str) -> str:
        for _ in range(10): 
            short_url = ''.join(random.choices(self.CHARACTERS, k=self.SHORT_URL_LENGTH))
            if not await self._url_exists(db, long_url):
                new_url = URL(long_url=str(long_url), short_url=short_url)
                db.add(new_url)
                await db.commit()
                return short_url
        raise ValueError("Could not generate unique short URL")
    
    async def get_original_url(self, db: AsyncSession, short_url: str) -> str:
        result = await db.execute(select(URL).where(URL.short_url == short_url))
        url_obj = result.scalar_one_or_none()
        if not url_obj:
            raise ValueError("Short URL not found")
        url_obj.clicks += 1
        await db.commit()
        return url_obj.long_url
