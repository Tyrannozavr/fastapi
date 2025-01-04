import asyncio
import time

from fastapi import FastAPI
from fastapi import Request, Response
from fastapi.exception_handlers import (
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.exceptions.exceptions import MyExcellentException
from api.exceptions.handlers import my_exception_handler, http_error_handler
from api.routers.api import router
from core.middlewares import AddProcessTimeHeaderMiddleware
from db.database import create_database
from models.doc_example import create_db_and_tables
from models.user import Base

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



# Call the create_database function
if __name__ == "__main__":
    asyncio.run(create_database())

# app.include_router(doc_example.database_router, prefix="/database", tags=["auth"])
app.include_router(router)

# @app.exception_handler(RequestValidationError)
# @app.exception_handler(MyExcellentException)
app.add_exception_handler(MyExcellentException, my_exception_handler)
app.add_exception_handler(MyExcellentException, http_error_handler)

app.add_middleware(AddProcessTimeHeaderMiddleware)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
