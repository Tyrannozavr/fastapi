from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing.suite.test_reflection import users

from models.user import User
from schemas.user import UserCreate


async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user(db: AsyncSession, user_id: int):
    result = await db.get(User, user_id)
    return result

async def get_users(db: AsyncSession) -> [User]:
    stmt = select(User)
    users = await db.scalars(stmt)
    # result = await db.execute(stmt)
    # users = result.scalars().all()
    result = await db.execute(stmt)
    users = result.scalars()
    a = result.scalars().all()
    print(a)
    return users

async def get_user_by_email(db: AsyncSession, email: str):
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user = result.scalars().first()
    return user