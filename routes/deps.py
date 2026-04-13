from fastapi.security import OAuth2PasswordBearer

from db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="")

async def get_database():
    async for db in get_db():
        yield db

def get_current_user():
    pass