from fastapi import APIRouter, Body, Depends, Cookie
from typing import Annotated

router =  APIRouter()


class BodyDependencies:
    def __init__(self, name: Annotated[str, Body]):
        self.name = name

@router.post("/hello", tags=["class"])
def hello(body: Annotated[BodyDependencies, Depends()]):
    return {"message": f"Hello World: {body.name}"}


def query_extractor(q: str | None = None):
    return q


def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
) -> str:
    if not q:
        return last_query
    return q


@router.get("/items/")
async def read_query(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor, use_cache=False)],
):
    """In this particular case use_cache parameter is completely useless,
    but I want to memorize that it is possible"""
    return {"q_or_cookie": query_or_default}