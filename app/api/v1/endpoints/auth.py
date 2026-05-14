from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_token
from app.core.config import settings
from app.api.deps import UserServiceDep, SessionDep
from app.db.model_url import User
from app.schemas.user import Token

router = APIRouter(tags=["login"])


@router.post("/login/access-token")
async def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserServiceDep,
    db: SessionDep,
):
    user: User = await user_service.authenticate_user(
        email=form_data.username, password=form_data.password, db=db
    )

    if not user:
        raise HTTPException("Incorrect email or password")
    elif not user.is_active:
        raise HTTPException("Inactive User")

    access_token_user = create_access_token(
        user.id, settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return Token(access_token=access_token_user)
