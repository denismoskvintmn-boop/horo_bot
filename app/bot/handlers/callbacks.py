from datetime import date

from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.deepseek_client import DeepSeekClient
from app.bot.keyboards.menu import get_main_menu_keyboard
from app.bot.messages.templates import HOROSCOPE_TEMPLATE, NOT_REGISTERED
from app.services.horoscope_service import HoroscopeService
from app.services.user_service import UserService

router = Router()


@router.callback_query(F.data == "horoscope")
async def callback_horoscope(callback: CallbackQuery, session: AsyncSession) -> None:
    user_service = UserService(session)
    try:
        user = await user_service.get_user_by_telegram_id(callback.from_user.id)
    except Exception:
        await callback.message.answer(NOT_REGISTERED)  # type: ignore[union-attr]
        await callback.answer()
        return

    await callback.message.answer("Generating your horoscope... please wait.")  # type: ignore[union-attr]

    try:
        deepseek_client = DeepSeekClient()
        horoscope_service = HoroscopeService(session, deepseek_client)
        horoscope = await horoscope_service.generate_horoscope(user, date.today())

        await callback.message.answer(  # type: ignore[union-attr]
            HOROSCOPE_TEMPLATE.format(
                name=user.name,
                date=horoscope.date,
                horoscope_text=horoscope.text,
            )
        )
    except Exception as e:
        await callback.message.answer(f"Error: {e}")  # type: ignore[union-attr]

    await callback.answer()


@router.callback_query(F.data == "profile")
async def callback_profile(callback: CallbackQuery, session: AsyncSession) -> None:
    user_service = UserService(session)
    try:
        user = await user_service.get_user_by_telegram_id(callback.from_user.id)
        from app.bot.messages.templates import PROFILE_TEMPLATE

        await callback.message.answer(  # type: ignore[union-attr]
            PROFILE_TEMPLATE.format(
                name=user.name,
                username=user.username or "N/A",
                gender=user.gender,
                birth_date=user.birth_date,
                birth_time=user.birth_time or "N/A",
                birth_city=user.birth_city,
                timezone=user.timezone,
                created_at=user.created_at.strftime("%Y-%m-%d")
                if user.created_at
                else "N/A",
            )
        )
    except Exception:
        await callback.message.answer(NOT_REGISTERED)  # type: ignore[union-attr]

    await callback.answer()


@router.callback_query(F.data == "help")
async def callback_help(callback: CallbackQuery) -> None:
    await callback.message.answer(  # type: ignore[union-attr]
        "Commands:\n"
        "/start - Start the bot\n"
        "/register - Create your profile\n"
        "/horoscope - Get your daily horoscope\n"
        "/profile - View your profile"
    )
    await callback.answer()
