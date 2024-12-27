from fastapi import APIRouter, Body, Depends
from typing import Annotated

router =  APIRouter()


class BodyDependencies:
    def __init__(self, name: Annotated[str, Body]):
        self.name = name

@router.post("/hello", tags=["class"])
def hello(body: Annotated[BodyDependencies, Depends()]):
    return {"message": f"Hello World: {body.name}"}