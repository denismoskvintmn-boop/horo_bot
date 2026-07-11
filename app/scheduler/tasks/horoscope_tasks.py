import asyncio
import logging
from asyncio import Semaphore
from datetime import date, datetime

from aiogram import Bot
from redis.asyncio import aioredis

from app.ai.deepseek_client import DeepSeekClient
from app.bot.messages.templates import HOROSCOPE_TEMPLATE
from app.core.config import settings
from app.database.database import async_session_factory
from app.database.repositories.horoscope_repository import HoroscopeRepository
from app.database.repositories.user_repository import UserRepository
from app.services.horoscope_service import HoroscopeService
from app.services.user_service import UserService

logger = logging.getLogger(__name__)


async def send_daily_horoscopes() -> None:
    """Send daily horoscopes to all active users."""
    logger.info("Starting daily horoscope distribution...")

    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN.get_secret_value())

    try:
        async with async_session_factory() as db:
            user_service = UserService(db)
            deepseek_client = DeepSeekClient()
            horoscope_service = HoroscopeService(db, deepseek_client)

            users = await user_service.repo.get_active_users()
            today = date.today()

            semaphore = Semaphore(20)

            async def process_user(user: object) -> None:
                async with semaphore:
                    try:
                        existing = await horoscope_service.repo.get_by_user_and_date(
                            user.id, today  # type: ignore[union-attr]
                        )
                        if existing and existing.status == "sent":
                            return

                        horoscope_obj = await horoscope_service.generate_horoscope(
                            user, today  # type: ignore[union-attr]
                        )

                        await bot.send_message(
                            user.telegram_id,  # type: ignore[union-attr]
                            HOROSCOPE_TEMPLATE.format(
                                name=user.name,  # type: ignore[union-attr]
                                date=horoscope_obj.date,
                                horoscope_text=horoscope_obj.text,
                            ),
                        )

                        horoscope_obj.status = "sent"
                        horoscope_obj.sent_at = datetime.now()
                        await db.commit()

                        logger.info(
                            "Horoscope sent to user %s", user.id  # type: ignore[union-attr]
                        )

                    except Exception as e:
                        logger.error(
                            "Error sending horoscope to user %s: %s",
                            user.id,  # type: ignore[union-attr]
                            e,
                        )

                    await asyncio.sleep(0.05)

            await asyncio.gather(*[process_user(user) for user in users])

        logger.info("Daily horoscope distribution completed.")

    finally:
        await bot.session.close()
