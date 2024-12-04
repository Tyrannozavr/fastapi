from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from schemas.user import UserCreate


async def create_user(db: AsyncSession, user: UserCreate):
    # db_user = User(**user.model_dump())
    db_user = User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user(db: AsyncSession, user_id: int):
    result = await db.get(User, user_id)
    return result

