from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

from auth import get_current_user, User, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, \
    fake_users_db

router = APIRouter()

AuthorizedUserType = Annotated[User, Depends(get_current_user)]

@router.get("/me", tags=["test1"], response_model=dict[str, User])
def items_secured(user: AuthorizedUserType):
    return {"user": user}


def get_user(user: AuthorizedUserType):
    return user

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/token")
async def get_token(form_data:  Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(fake_db=fake_users_db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type='bearer')
