import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.redis import RedisStorage
from redis import asyncio as aioredis

from app.bot.handlers import callbacks, horoscope, profile, start
from app.bot.middlewares.logging import LoggingMiddleware
from app.bot.middlewares.throttling import ThrottlingMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.database.session import DatabaseMiddleware

logger = logging.getLogger(__name__)


async def on_startup() -> None:
    logger.info("Bot starting up...")
    # Check Redis connection
    try:
        redis = aioredis.from_url(settings.REDIS_URL)
        await redis.ping()
        await redis.close()
        logger.info("Redis connection OK")
    except Exception as e:
        logger.error("Redis connection failed: %s", e)

    # Check database connection
    try:
        from app.database.database import async_session_factory

        async with async_session_factory() as session:
            await session.execute(
                __import__("sqlalchemy").text("SELECT 1")
            )
        logger.info("Database connection OK")
    except Exception as e:
        logger.error("Database connection failed: %s", e)


async def on_error(event: types.ErrorEvent) -> None:
    logger.error(
        "Update error: %s\nCause: %s",
        event.update,
        event.exception,
        exc_info=True,
    )


async def main() -> None:
    setup_logging()
    logger.info("Starting bot...")

    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN.get_secret_value())

    redis = aioredis.from_url(settings.REDIS_URL)
    storage = RedisStorage(redis)

    dp = Dispatcher(storage=storage)

    # Error handler
    dp.error.register(on_error)

    # Middleware - order matters!
    dp.message.middleware(DatabaseMiddleware())
    dp.message.middleware(LoggingMiddleware())
    dp.message.middleware(ThrottlingMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())

    # Routers
    dp.include_router(start.router)
    dp.include_router(horoscope.router)
    dp.include_router(profile.router)
    dp.include_router(callbacks.router)

    dp.startup.register(on_startup)

    logger.info("Bot initialized. Starting polling...")

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error("Bot polling error: %s", e, exc_info=True)
    finally:
        await bot.session.close()
        await redis.close()


if __name__ == "__main__":
    asyncio.run(main())
