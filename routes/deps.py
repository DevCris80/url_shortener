from fastapi.security import OAuth2PasswordBearer

from db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_database():
    async for db in get_db():
        yield db

async def get_current_user():
    pass