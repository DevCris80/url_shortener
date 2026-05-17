from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.url import URLCreate, URLInfo, URLResponse
from app.api.deps import SessionDep, CurrentUser, UserServiceDep
from app.service.shorten import Shortener

router = APIRouter()
shortener = Shortener()

@router.post("/shortener", response_model=URLResponse)
async def shorten_url(url: URLCreate, current_user: CurrentUser, db: SessionDep):
    try:
        short_url = await shortener.short_url(db=db, url_create=url, user_id=current_user.id)
        return short_url
    except ValueError:
        raise HTTPException(400, detail='Not possible')

@router.get("/urls", response_model=list[URLInfo])
async def list_url(user_service: UserServiceDep, current_user: CurrentUser, db: SessionDep):
    urls = await user_service.get_url_user(current_user.id, db)
    return urls

@router.get("/{short_url}")
async def get_original_url(short_url: str, db: SessionDep):
    long_url = await shortener.get_original_url(db, short_url)
    return RedirectResponse(url = long_url, status_code=301)