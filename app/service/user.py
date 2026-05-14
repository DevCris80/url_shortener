from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.schemas.user import UserCreate
from app.db.model_url import User
from app.core.security import verify_password, get_password_hash
from app.exceptions import user_exceptions


class UserService:
    def __init__(self):
        self.DUMMY_PASSWORD_HASH = (
            "$argon2id$v=19$m=65536,t=3,p=4$ZGFtbXlTYWx0$ZGFtbXlIYXNo"
        )

    async def create_user(self, new_user: UserCreate, db: AsyncSession):
        existing_user = await self.get_user_by_email(email=new_user.email, db=db)
        if existing_user:
            raise user_exceptions.UserAlreadyExistsError(field= "email", value=new_user.email)
        
        pasword_hash_user = get_password_hash(new_user.password)
        db_user = User(
            **new_user,
            pasword_hash = pasword_hash_user
        )

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
        

    async def get_user_by_id(self, user_id: int, db: AsyncSession):
        return await db.get(User, user_id)

    async def get_user_by_email(self, email: str, db: AsyncSession):
        return await db.query(User).filter(User.email == email).first()

    async def authenticate_user(self, email: str, password: str, db: AsyncSession):
        user = await self.get_user_by_email(email, db)
        if not user:
            verify_password(password, self.DUMMY_PASSWORD_HASH)
            return None

        is_valid, new_hash = verify_password(password, user.password_hash)
        if not is_valid:
            return None

        if new_hash:
            user.password_hash = new_hash
            db.add(user)
            await db.commit()
            await db.refresh(user)

        return user

    async def get_url_user(self, user_id: int, db: AsyncSession):
        query = select(User).options(selectinload(User.urls)).where(User.id == user_id)

        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            return None

        return user.urls
