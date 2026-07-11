from datetime import date

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.deepseek_client import DeepSeekClient
from app.bot.messages.templates import HOROSCOPE_TEMPLATE, NOT_REGISTERED
from app.services.horoscope_service import HoroscopeService
from app.services.user_service import UserService

router = Router()


@router.message(Command("horoscope"))
@router.message(F.text == "Get Horoscope")
async def cmd_horoscope(message: Message, session: AsyncSession) -> None:
    user_service = UserService(session)
    try:
        user = await user_service.get_user_by_telegram_id(message.from_user.id)  # type: ignore[union-attr]
    except Exception:
        await message.answer(NOT_REGISTERED)
        return

    await message.answer("Generating your horoscope... please wait.")

    try:
        deepseek_client = DeepSeekClient()
        horoscope_service = HoroscopeService(session, deepseek_client)
        horoscope = await horoscope_service.generate_horoscope(user, date.today())

        await message.answer(
            HOROSCOPE_TEMPLATE.format(
                name=user.name,
                date=horoscope.date,
                horoscope_text=horoscope.text,
            )
        )
    except Exception as e:
        await message.answer(f"Error generating horoscope: {e}")
