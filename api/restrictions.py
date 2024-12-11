from fastapi import APIRouter, Path
from fastapi import Query, Cookie
from typing import Annotated, Literal

from pydantic import BaseModel, Field

from my_types.query import FilterParams

router = APIRouter()

@router.get("/parameters/{route}/")
def test_parameters(route: str, query: Annotated[str | None, Query(max_length=50)], metadata: Annotated[str | None, Cookie(max_length=30)] = None):
    return f"route is {route}, query is {query} metadata is {metadata}"

@router.get("/impossible")
def test_parameters(query: Annotated[str | None, Query(max_length=5)] = "helloworld"):
    return f"query is {query}"

@router.get("/list")
def test_list_parameter(lst: Annotated[list[str], Query(title="test_title",
                                                        description="description for list parameter",
                                                        alias="hello-world-example", deprecated=True)],
                        test: Annotated[str | None, Query(include_in_schema=False)] = None):
    response = {"query items are": lst}
    if test:
        response["secret parameter is"] = test
    return response



@router.get("/bad_approach/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    """better with annotated"""
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

@router.get("/number/validation/{number}")
def validate_number(number: Annotated[int, Path(ge=4, le=1000)], size: Annotated[float, Query(gt=0, lt=10.5)]):
    return f"number is {number} and size is {size}"


@router.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query