import asyncio


from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from api.user import get_db, get_db_session
from crud.houses import create_house, add_house_to_street
from database.database import DATABASE_URL_TEST
from models.user import User

engine = create_async_engine(DATABASE_URL_TEST, echo=False)

async_session = async_sessionmaker(engine, expire_on_commit=False)

async def main():
    async with async_session() as session:
        try:
            # home = create_house(db=session, home_name="MyHouse", street_name="VulBChausskaya")
            street = await add_house_to_street(db=session, street_name="VulBChausskaya", house_name="first_house")
            print(street)
        except Exception as e:
            print("error", e)
            await session.rollback()
        finally:
            await session.commit()

        # stmt = select(User).where(User.pk == 1)
        # result = await session.execute(stmt)
    # session = get_db_session()

asyncio.run(main())