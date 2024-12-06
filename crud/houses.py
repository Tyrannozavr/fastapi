from sqlalchemy.ext.asyncio import AsyncSession

from models.user import Home, Street


def create_house(db: AsyncSession, home_name: str, street_name: str | None) -> Home:
    home = Home(name=home_name)
    if street_name:
        home.street = Street(name=street_name)
    db.add(home)
    return home
