from db.session import get_db

async def get_database():
    async for db in get_db():
        yield db