import json
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.deepseek_client import DeepSeekClient
from app.core.exceptions import HoroscopeAlreadyExistsError
from app.database.models import Horoscope, User
from app.database.repositories.horoscope_repository import HoroscopeRepository
from app.services.astronomy_service import AstronomyService


class HoroscopeService:
    def __init__(self, db: AsyncSession, deepseek_client: DeepSeekClient) -> None:
        self.repo = HoroscopeRepository(db)
        self.astronomy_service = AstronomyService()
        self.deepseek = deepseek_client

    async def generate_horoscope(self, user: User, target_date: date) -> Horoscope:
        existing = await self.repo.get_by_user_and_date(user.id, target_date)
        if existing:
            raise HoroscopeAlreadyExistsError(
                f"Horoscope for user {user.id} on {target_date} already exists"
            )

        astronomy_data = await self.astronomy_service.get_astronomy_data(target_date)

        horoscope_text = await self.deepseek.generate_horoscope(
            user_data={
                "name": user.name,
                "gender": user.gender,
                "birth_date": user.birth_date.isoformat(),
                "birth_city": user.birth_city,
                "birth_time": user.birth_time.isoformat() if user.birth_time else None,
            },
            astronomy_data=astronomy_data,
        )

        horoscope = Horoscope(
            user_id=user.id,
            date=target_date,
            astronomy_json=json.dumps(astronomy_data),
            text=horoscope_text,
            status="pending",
        )

        return await self.repo.create(horoscope)
