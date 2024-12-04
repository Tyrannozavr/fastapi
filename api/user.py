from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# import crud, schemas
from crud import user as user_crud
from schemas import user as user_schemas
from database.database import async_session

router =  APIRouter()


async def get_db():
    async with async_session() as session:
        yield session


@router.post("/users/", response_model=user_schemas.User)
async def create_user(user: user_crud.UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_crud.create_user(db=db, user=user)

@router.get("/users/{user_id}", response_model=user_schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await user_crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user