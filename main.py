import asyncio

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from api import user, test, restrictions, files, dependencies
from api.exceptions import MyExcellentException
from database.database import engine
from models.user import Base
from fastapi import status
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
# app.include_router(user.router)
# app.include_router(test.router)
# app.include_router(restrictions.router)
# app.include_router(files.router)
app.include_router(dependencies.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)

@app.exception_handler(MyExcellentException)
def my_exception_handler(request, exc: MyExcellentException):
    return JSONResponse(
        status_code=404,
        content=f"OMG! An HTTP error!: {exc.name}"
    )
