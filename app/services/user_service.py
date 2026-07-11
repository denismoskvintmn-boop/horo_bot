from datetime import date, time

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.database.models import User
from app.database.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.repo = UserRepository(db)

    async def register_user(
        self,
        telegram_id: int,
        username: str | None,
        name: str,
        gender: str,
        birth_date: date,
        birth_city: str,
        birth_time: time | None = None,
        timezone: str = "UTC",
    ) -> User:
        existing = await self.repo.get_by_telegram_id(telegram_id)
        if existing:
            raise UserAlreadyExistsError(f"User with telegram_id {telegram_id} already exists")

        user = User(
            telegram_id=telegram_id,
            username=username,
            name=name,
            gender=gender,
            birth_date=birth_date,
            birth_time=birth_time,
            birth_city=birth_city,
            timezone=timezone,
        )
        return await self.repo.create(user)

    async def get_user_by_telegram_id(self, telegram_id: int) -> User:
        user = await self.repo.get_by_telegram_id(telegram_id)
        if not user:
            raise UserNotFoundError(f"User with telegram_id {telegram_id} not found")
        return user
