from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep, CurrentUser, UserServiceDep
from app.schemas.user import UserCreate
from app.exceptions import user_exceptions

router = APIRouter()

@router.post("/")
async def create_user(
    user: UserCreate,
    db: SessionDep,
    user_service: UserServiceDep
):
    try:
        return user_service.create_user(user, db)
    except user_exceptions.UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail="User already exists")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error in create user")

@router.get("/me")
async def read_user_me(current_user: CurrentUser):
    return current_user
