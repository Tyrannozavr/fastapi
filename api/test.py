from fastapi import APIRouter
from sqlalchemy import select
from models.user import User
from enum import Enum
router = APIRouter()


@router.get("/")
async def main():
    return {"message": "Hello, world"}

@router.get("/second")
async def second():
    return "helloworld"

@router.get("/orm")
def get_orm() -> str:
    stmt = select(User)
    return str(stmt)

@router.get("/items/{item_id}")
def get_item_by_id(item_id: int | float):
    return {"item_id": item_id}


class PredefinedUsernames(Enum):
    username1 = "dmiv"
    username2 = "tyrannozavr"

@router.get("/predefined/{username}")
def get_predefined_parameter(username: PredefinedUsernames):
    return f"Hello, {username.value}"