import time
from collections import defaultdict
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

THROTTLE_SECONDS = 1.0


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.last_call: dict[int, float] = defaultdict(float)

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id if event.from_user else 0
        now = time.time()

        if now - self.last_call[user_id] < THROTTLE_SECONDS:
            await event.answer("Please wait a moment before sending another message.")
            return None

        self.last_call[user_id] = now
        return await handler(event, data)
