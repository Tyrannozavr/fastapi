from typing import List

from sqlalchemy import Column, Integer, String, select, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


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


class Home(Base):
    __tablename__ = "home"
    name: Mapped[str] = mapped_column(String(30))
    street_id: Mapped[int] = mapped_column(ForeignKey("streets.pk"))

    street: Mapped["Street"] = relationship(back_populates="houses")


class Street(Base):
    __tablename__ = "streets"
    name: Mapped[str] = mapped_column(String(30))

    houses: Mapped[List["Home"]] = relationship(back_populates="street", cascade="all, delete-orphan")
