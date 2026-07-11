from datetime import date

from sqlalchemy import select

from app.database.models import Horoscope
from app.database.repositories.base import BaseRepository


class HoroscopeRepository(BaseRepository[Horoscope]):
    def __init__(self, db):  # type: ignore[no-untyped-def]
        super().__init__(Horoscope, db)

    async def get_by_user_and_date(self, user_id: int, target_date: date) -> Horoscope | None:
        result = await self.db.execute(
            select(Horoscope).where(Horoscope.user_id == user_id, Horoscope.date == target_date)
        )
        return result.scalar_one_or_none()
