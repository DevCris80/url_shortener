from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from schemas.url import URLCreate
from routes.deps import get_database
from service.shorten import Shortener
from db.model_url import URL

router = APIRouter()
shortener = Shortener()

@router.post("/shortener")
async def shorten_url(url: URLCreate, db: AsyncSession = Depends(get_database)):
    try:
        short_url = await shortener.short_url(db, url.long_url)
    except ValueError:
        raise HTTPException(400, detail='Not possible')
    return {"short_url": short_url}

@router.get("/urls")
async def list_url(db: AsyncSession = Depends(get_database)):
    list_url_db = await db.execute(select(URL).limit(10))
    return list_url_db.scalars().all()

        
@router.get("/{short_url}")
async def get_original_url(short_url: str, db: AsyncSession = Depends(get_database)):
    long_url = await shortener.get_original_url(db, short_url)
    return RedirectResponse(url = long_url, status_code=301)