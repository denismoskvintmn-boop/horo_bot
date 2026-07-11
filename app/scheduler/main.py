import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.config import settings
from app.core.logging import setup_logging
from app.scheduler.tasks.horoscope_tasks import send_daily_horoscopes

logger = logging.getLogger(__name__)


async def main() -> None:
    setup_logging()
    logger.info("Starting scheduler...")

    scheduler = AsyncIOScheduler(timezone=settings.TIMEZONE)

    hour, minute = settings.HOROSCOPE_SEND_TIME.split(":")
    scheduler.add_job(
        send_daily_horoscopes,
        trigger="cron",
        hour=int(hour),
        minute=int(minute),
        id="daily_horoscopes",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("Scheduler started. Daily horoscopes at %s", settings.HOROSCOPE_SEND_TIME)

    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler stopped.")


if __name__ == "__main__":
    asyncio.run(main())
