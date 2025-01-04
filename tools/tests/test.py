import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from db.queries.houses import add_house_to_street
from database.database import DATABASE_URL_TEST

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