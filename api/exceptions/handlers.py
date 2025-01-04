from fastapi import HTTPException
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response

from api.exceptions.exceptions import MyExcellentException


def my_exception_handler(request, exc: MyExcellentException):
    return JSONResponse(
        status_code=404,
        content=f"OMG! An HTTP error!: {exc.name}"
    )
# def my_exception_handler(request, exc: MyExcellentException):
#     return JSONResponse(
#         status_code=404,
#         content=f"OMG! An HTTP error!: {exc.name}"
#     )

async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)

async def http_error_handler(request: Request, exc: Exception) -> Response:
    if isinstance(exc, HTTPException):
        return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)
    return JSONResponse({"errors": [str(exc)]}, status_code=500)