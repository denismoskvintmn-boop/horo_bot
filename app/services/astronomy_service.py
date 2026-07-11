import json
from datetime import date

import redis.asyncio as aioredis

from app.astronomy.astrology import get_astronomy_data
from app.core.config import settings


class AstronomyService:
    def __init__(self) -> None:
        self.redis = aioredis.from_url(settings.REDIS_URL)
        self.cache_ttl = 86400  # 24 hours

    async def get_astronomy_data(self, target_date: date) -> dict:
        cache_key = f"astronomy:{target_date.isoformat()}"

        cached = await self.redis.get(cache_key)
        if cached:
            return json.loads(cached)

        data = get_astronomy_data(target_date)
        await self.redis.setex(cache_key, self.cache_ttl, json.dumps(data))
        return data

    async def close(self) -> None:
        await self.redis.close()
