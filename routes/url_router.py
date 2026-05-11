from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.url import URLCreate, URLInfo, URLResponse
from routes.deps import get_database
from service.shorten import Shortener

router = APIRouter()
shortener = Shortener()

@router.post("/shortener", response_model=URLResponse)
async def shorten_url(url: URLCreate, db: AsyncSession = Depends(get_database)):
    try:
        short_url = await shortener.short_url(db, url)
        return short_url
    except ValueError:
        raise HTTPException(400, detail='Not possible')

@router.get("/urls", response_model=list[URLInfo])
async def list_url(db: AsyncSession = Depends(get_database)):
    list_url_db = await shortener.list_urls(db)
    return list_url_db

        
@router.get("/{short_url}")
async def get_original_url(short_url: str, db: AsyncSession = Depends(get_database)):
    long_url = await shortener.get_original_url(db, short_url)
    return RedirectResponse(url = long_url, status_code=301)