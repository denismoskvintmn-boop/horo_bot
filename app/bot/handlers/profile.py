from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.messages.templates import NOT_REGISTERED, PROFILE_TEMPLATE
from app.services.user_service import UserService

router = Router()


@router.message(Command("profile"))
@router.message(F.text == "My Profile")
async def cmd_profile(message: Message, session: AsyncSession) -> None:
    user_service = UserService(session)
    try:
        user = await user_service.get_user_by_telegram_id(message.from_user.id)  # type: ignore[union-attr]
    except Exception:
        await message.answer(NOT_REGISTERED)
        return

    await message.answer(
        PROFILE_TEMPLATE.format(
            name=user.name,
            username=user.username or "N/A",
            gender=user.gender,
            birth_date=user.birth_date,
            birth_time=user.birth_time or "N/A",
            birth_city=user.birth_city,
            timezone=user.timezone,
            created_at=user.created_at.strftime("%Y-%m-%d") if user.created_at else "N/A",
        )
    )
