from datetime import date as date_type

from pydantic import BaseModel, Field


class HoroscopeResponse(BaseModel):
    """Schema for horoscope API response."""

    date: date_type = Field(..., description="Horoscope date")
    text: str = Field(..., description="Horoscope text")
    status: str = Field(..., description="Horoscope status (pending/sent/failed)")


class HoroscopeNotFoundResponse(BaseModel):
    """Schema when no horoscope found."""

    info: str = Field(..., description="Info message")
