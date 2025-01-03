from sqlmodel import SQLModel, Field

class SecondTable(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str = Field()
    last_name: str = Field()
