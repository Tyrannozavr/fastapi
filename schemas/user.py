from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    full_name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    pk: int

    class Config:
        from_attributes = True

