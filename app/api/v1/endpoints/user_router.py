from fastapi import APIRouter, Depends

from app.api.deps import CurrentUser

router = APIRouter()

@router.get("/me")
async def read_user_me(current_user: CurrentUser):
    return current_user