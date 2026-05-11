from sqlalchemy.ext.asyncio import AsyncSession

from db.model_url import User
from core.security import verify_password

async def get_user_by_id(user_id: int, db: AsyncSession):
    return await db.get(User, user_id)

async def get_user_by_email(email: str, db: AsyncSession):
    return await db.query(User).filter(User.email == email).first()

DUMMY_PASSWORD_HASH = "$argon2id$v=19$m=65536,t=3,p=4$ZGFtbXlTYWx0$ZGFtbXlIYXNo"

async def authenticate_user(email: str, password: str, db: AsyncSession):
    user = await get_user_by_email(email, db)
    if not user:
        verify_password(password, DUMMY_PASSWORD_HASH)
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

