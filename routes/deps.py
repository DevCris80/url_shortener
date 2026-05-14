from typing import Annotated

import jwt
from jwt import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from db.model_url import User
from db.session import get_db
from core.config import settings
from service.user import UserService as UserServiceClass
from service.shorten import Shortener as ShortenerClass

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/access-token")

async def get_database():
    async for db in get_db():
        yield db

SessionDep = Annotated[AsyncSession, Depends(get_database)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]

async def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data: str = payload.get("sub")
    except (InvalidTokenError, ValidationError):
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    user = await session.get(User, int(token_data))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

UserServiceDep = Annotated[UserServiceClass, Depends(lambda: UserServiceClass())]
ShortenerDep = Annotated[ShortenerClass, Depends(lambda: ShortenerClass())]