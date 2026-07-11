import re
from datetime import date, time


def validate_name(name: str) -> bool:
    return bool(name and len(name) >= 2 and len(name) <= 255)


def validate_gender(gender: str) -> bool:
    return gender in ("male", "female")


def validate_birth_date(birth_date: date) -> bool:
    return birth_date <= date.today()


def validate_birth_time(birth_time: time) -> bool:
    return True


def validate_city(city: str) -> bool:
    return bool(city and len(city) >= 2 and len(city) <= 255)


def validate_telegram_id(telegram_id: int) -> bool:
    return telegram_id > 0


def validate_date_format(date_str: str) -> bool:
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(pattern, date_str):
        return False
    try:
        date.fromisoformat(date_str)
        return True
    except ValueError:
        return False
