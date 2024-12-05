import asyncio


from fastapi.params import Depends
from sqlalchemy import select

from api.user import get_db, get_db_session
from database.database import async_session
from models.user import User


async def main():
    async with async_session() as session:
        print(session, type(session))
        stmt = select(User).where(User.pk == 1)
        result = await session.execute(stmt)
        user = result.scalars().first()
        print(user.email, user.pk)
    session = get_db_session()
    print(session, type(session))

asyncio.run(main())