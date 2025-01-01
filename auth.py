from datetime import timedelta, datetime, timezone
from typing import Annotated

import jwt
from fastapi import HTTPException
from fastapi import status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
SECRET_KEY = '92a0b48a5450a2ad8ca84a7bd9c115e414521a4404cb42437e9ae89eaf28b01e'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(plaintext_password: str) -> str:
    return pwd_context.hash(plaintext_password)

def verify_password(plaintext_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plaintext_password, hashed_password)

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

fake_users_db = {
    "dmiv": {
        "username": "dmiv",
        "full_name": "Dzmitry Schyslionako",
        "email": "dimon@gmail.com",
        "hashed_password": "$2b$12$7mA9/MsqwbpnG5mDdY88OujvkDEtDmwnC8DEWcqImOviYAg3RwrDi",
        "disabled": False,
    }
}

class UserInDB(User):
    hashed_password: str

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload_data.get('sub')
    user = get_user(fake_users_db, username=username)
    if not user:
        raise credentials_exception
    return user

def get_user(fake_db: dict, username: str) -> UserInDB | None:
    if username in fake_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)

async def authenticate_user(fake_db: dict, username: str, password: str) -> bool | UserInDB:
    user = get_user(fake_db, username=username)
    if not user:
        return False
    if not verify_password(plaintext_password=password, hashed_password=user.hashed_password):
        return False
    return user
