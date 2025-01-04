from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from models.user import Base

DATABASE_URL_TEST = "sqlite+aiosqlite:///../aiosqlite.sqlite"
DATABASE_URL = "sqlite+aiosqlite:///aiosqlite.sqlite"

engine = create_async_engine(DATABASE_URL, echo=False)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_database():
    async with engine.begin() as conn:
        # This will create all tables based on your models
        await conn.run_sync(Base.metadata.create_all)