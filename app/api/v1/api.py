from fastapi import APIRouter
from app.api.v1.endpoints import url_router, user_router, auth

api_router = APIRouter()

api_router.include_router(auth.router, tags=["login"])
api_router.include_router(user_router.router, prefix="/users", tags=["users"])
api_router.include_router(url_router.router, tags=["urls"])
