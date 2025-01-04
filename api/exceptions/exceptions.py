from typing import Any

from fastapi import HTTPException


class MyExcellentException(HTTPException):
    def __init__(self, name: str|None = None, status_code: int = 500, detail: Any = None):
        self.name = name
        self.status_code = status_code
        self.detail = detail

