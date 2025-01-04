from pydantic import BaseModel, Field

class BaseUser(BaseModel):
    username: str = Field(max_length=20)
    email: str = Field(max_length=20)

class UserIn(BaseUser):
    password: str = Field(max_length=20)


class UserOut(BaseModel):
    pass
