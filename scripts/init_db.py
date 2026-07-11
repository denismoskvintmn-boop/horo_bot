import asyncio

from app.database.database import engine
from app.database.models import Base


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created.")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_db())
