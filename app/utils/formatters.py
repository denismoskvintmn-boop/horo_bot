from datetime import date, datetime


def format_date(d: date) -> str:
    return d.strftime("%Y-%m-%d")


def format_datetime(dt: datetime | None) -> str:
    if dt is None:
        return "N/A"
    return dt.strftime("%Y-%m-%d %H:%M")


def format_horoscope_text(text: str, max_length: int = 4000) -> str:
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def format_gender(gender: str) -> str:
    return "Male" if gender == "male" else "Female"
