import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.ai.prompts import SYSTEM_PROMPT, build_user_prompt
from app.core.config import settings
from app.core.exceptions import DeepSeekAPIError


class DeepSeekClient:
    def __init__(self) -> None:
        self.api_key = settings.DEEPSEEK_API_KEY.get_secret_value()
        self.api_url = settings.DEEPSEEK_API_URL

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPStatusError)),
    )
    async def generate_horoscope(
        self, user_data: dict, astronomy_data: dict
    ) -> str:
        prompt = build_user_prompt(user_data, astronomy_data)

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.api_url,
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000,
                },
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )

            response.raise_for_status()
            data = response.json()

            if "choices" not in data or len(data["choices"]) == 0:
                raise DeepSeekAPIError("No choices in DeepSeek response")

            return data["choices"][0]["message"]["content"]
