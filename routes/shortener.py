from fastapi import APIRouter, Depends

from schemas.url import URL
from routes.deps import get_db

router = APIRouter()


@router.post("/shorten")
def shorten_url(url: URL, db = Depends(get_db)):
    return url