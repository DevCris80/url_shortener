from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from routes.deps import get_database, get_current_user
from schemas.user import UserRead

router = APIRouter()

@router.get("/me")
async def read_user_me(current_user = Annotated[UserRead, Depends(get_current_user)]):
    return "Hello World"