from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

DATABASE_URL_TEST = "sqlite+aiosqlite:///../aiosqlite.sqlite"
DATABASE_URL = "sqlite+aiosqlite:///aiosqlite.sqlite"

engine = create_async_engine(DATABASE_URL, echo=False)

async_session = async_sessionmaker(engine, expire_on_commit=False)


