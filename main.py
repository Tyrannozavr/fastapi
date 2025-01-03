import asyncio
import time

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware

from api import user, test, restrictions, files, dependencies, auth
from api.exceptions import MyExcellentException
from database.database import engine
from models import doc_example
from models.doc_example import create_db_and_tables
from models.user import Base
from fastapi import status
app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=30
) # It's for cross origins only, all methods/headers/e.t. will be allowed from the same origin

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
# app.include_router(dependencies.router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(doc_example.database_router, prefix="/database", tags=["auth"])


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

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response: Response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
