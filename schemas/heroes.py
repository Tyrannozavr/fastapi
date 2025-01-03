from sqlmodel import SQLModel, Field


class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str


class HeroCreate(HeroBase):
    secret_name: str

class HeroPublic(HeroBase):
    id: int


class HeroUpdate(HeroBase):
    name: str | None = Field(default=None)
    age: int | None = Field(default=None)
    secret_name: str | None = Field(default=None)


class Test(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
