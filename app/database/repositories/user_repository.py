from sqlalchemy import select

from app.database.models import User
from app.database.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db):  # type: ignore[no-untyped-def]
        super().__init__(User, db)

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()

    async def get_active_users(self) -> list[User]:
        result = await self.db.execute(select(User).where(User.is_active == True))  # noqa: E712
        return list(result.scalars().all())
