import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.menu import get_gender_keyboard, get_main_menu_keyboard
from app.bot.messages.templates import (
    ALREADY_REGISTERED,
    NOT_REGISTERED,
    REGISTRATION_COMPLETE,
    WELCOME_MESSAGE,
)
from app.core.security import escape_user_input
from app.services.user_service import UserService

logger = logging.getLogger(__name__)
router = Router()


class RegistrationState(StatesGroup):
    name = State()
    gender = State()
    birth_date = State()
    birth_city = State()
    birth_time = State()


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession, state: FSMContext) -> None:
    try:
        user_service = UserService(session)
        try:
            await user_service.get_user_by_telegram_id(message.from_user.id)  # type: ignore[union-attr]
            await message.answer(ALREADY_REGISTERED, reply_markup=get_main_menu_keyboard())
            return
        except Exception:
            pass

        await message.answer(WELCOME_MESSAGE)
        await state.set_state(RegistrationState.name)
        await message.answer("What is your name?")
    except Exception as e:
        logger.error("Error in cmd_start: %s", e, exc_info=True)
        await message.answer("An error occurred. Please try again.")


@router.message(RegistrationState.name)
async def process_name(message: Message, state: FSMContext) -> None:
    try:
        name = escape_user_input(message.text or "")
        await state.update_data(name=name)
        await state.set_state(RegistrationState.gender)
        await message.answer(
            f"Nice to meet you, {name}! What is your gender?",
            reply_markup=get_gender_keyboard(),
        )
    except Exception as e:
        logger.error("Error in process_name: %s", e, exc_info=True)
        await message.answer("An error occurred. Please try /start again.")


@router.callback_query(F.data.startswith("gender:"))
async def process_gender(callback, state: FSMContext) -> None:  # type: ignore[no-untyped-def]
    try:
        gender = callback.data.split(":")[1]
        await state.update_data(gender=gender)
        await state.set_state(RegistrationState.birth_date)
        await callback.message.answer("When were you born? (YYYY-MM-DD)")  # type: ignore[union-attr]
        await callback.answer()
    except Exception as e:
        logger.error("Error in process_gender: %s", e, exc_info=True)
        await callback.answer("An error occurred.")


@router.message(RegistrationState.birth_date)
async def process_birth_date(message: Message, state: FSMContext) -> None:
    try:
        from datetime import date

        try:
            birth_date = date.fromisoformat(message.text or "")
        except ValueError:
            await message.answer("Invalid format. Please use YYYY-MM-DD:")
            return

        await state.update_data(birth_date=birth_date.isoformat())
        await state.set_state(RegistrationState.birth_city)
        await message.answer("In which city were you born?")
    except Exception as e:
        logger.error("Error in process_birth_date: %s", e, exc_info=True)
        await message.answer("An error occurred. Please try /start again.")


@router.message(RegistrationState.birth_city)
async def process_birth_city(message: Message, state: FSMContext) -> None:
    try:
        city = escape_user_input(message.text or "")
        await state.update_data(birth_city=city)
        await state.set_state(RegistrationState.birth_time)
        await message.answer(
            "What time were you born? (HH:MM, or skip by typing 'skip')"
        )
    except Exception as e:
        logger.error("Error in process_birth_city: %s", e, exc_info=True)
        await message.answer("An error occurred. Please try /start again.")


@router.message(RegistrationState.birth_time)
async def process_birth_time(
    message: Message, state: FSMContext, session: AsyncSession
) -> None:
    try:
        from datetime import time

        data = await state.get_data()
        birth_time = None

        if message.text and message.text.lower() != "skip":
            try:
                parts = message.text.split(":")
                birth_time = time(int(parts[0]), int(parts[1]))
            except (ValueError, IndexError):
                await message.answer("Invalid format. Please use HH:MM or 'skip':")
                return

        user_service = UserService(session)
        user = await user_service.register_user(
            telegram_id=message.from_user.id,  # type: ignore[union-attr]
            username=message.from_user.username,  # type: ignore[union-attr]
            name=data["name"],
            gender=data["gender"],
            birth_date=data["birth_date"],
            birth_city=data["birth_city"],
            birth_time=birth_time,
        )

        await state.clear()
        await message.answer(
            REGISTRATION_COMPLETE.format(
                name=user.name,
                gender=user.gender,
                birth_date=user.birth_date,
                birth_city=user.birth_city,
            ),
            reply_markup=get_main_menu_keyboard(),
        )
    except Exception as e:
        logger.error("Error in process_birth_time: %s", e, exc_info=True)
        await message.answer(f"Registration error: {e}")
