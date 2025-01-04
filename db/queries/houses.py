from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, selectinload

from models.user import Home, Street


def create_house(db: AsyncSession, home_name: str, street_name: str | None) -> Home:
    home = Home(name=home_name)
    if street_name:
        home.street = Street(name=street_name)
    db.add(home)
    return home

async def add_house_to_street(db: AsyncSession, street_name: str, house_name: str) -> Street:
    result = await db.execute(select(Street).options(selectinload(Street.houses)).where(Street.name == street_name))
    street = result.scalar_one_or_none()
    if not street:
        street = Street(name=street_name)
        db.add(street)
    result = await db.execute(select(Home).where(Home.name == house_name))
    house = result.scalar_one_or_none()
    if not house:
        house = Home(name=house_name, street_id=street.pk)
        db.add(house)
    elif house not in street.houses:
        street.houses.append(house)
    return street