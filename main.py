import asyncio

from fastapi import FastAPI
from database.database import engine
from models.user import Base
from api import user

app = FastAPI()

# Create the database tables
# Base.metadata.create_all(bind=engine)

async def create_database():
    async with engine.begin() as conn:
        # This will create all tables based on your models
        await conn.run_sync(Base.metadata.create_all)

# Call the create_database function
if __name__ == "__main__":
    asyncio.run(create_database())
app.include_router(user.router)

