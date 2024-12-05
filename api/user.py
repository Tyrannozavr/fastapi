from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession

# import crud, schemas
from crud import user as user_crud
from schemas import user as user_schemas
from database.database import async_session

router =  APIRouter()


async def get_db():
    async with async_session() as session:
        yield session

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    factory = async_session
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError as error:
            await session.rollback()
            raise

@router.post("/users/", response_model=user_schemas.User)
async def create_user(user: user_crud.UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_crud.create_user(db=db, user=user)

@router.get("/users/id/{user_id}", response_model=user_schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await user_crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/email/{user_email}", response_model=user_schemas.User)
async def read_user_by_email(user_email: str, db: AsyncSession = Depends(get_db)):
    db_user = await user_crud.get_user_by_email(db=db, email=user_email)
    return db_user