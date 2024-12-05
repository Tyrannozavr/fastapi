from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase



# Base = declarative_base()

class Base(DeclarativeBase):
    pk: Mapped[int] = mapped_column(primary_key=True)

class User(Base):
    __tablename__ = 'users'

    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, index=True)

class Test(Base):
    __tablename__ = "test_table"

    name: Mapped[str] = mapped_column(String)