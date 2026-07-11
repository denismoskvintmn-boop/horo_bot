from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Get Horoscope", callback_data="horoscope"),
                InlineKeyboardButton(text="My Profile", callback_data="profile"),
            ],
            [
                InlineKeyboardButton(text="Help", callback_data="help"),
            ],
        ]
    )


def get_gender_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Male", callback_data="gender:male"),
                InlineKeyboardButton(text="Female", callback_data="gender:female"),
            ],
        ]
    )
