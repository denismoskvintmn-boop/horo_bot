from datetime import date

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    """Schema for user API response."""

    id: int = Field(..., description="User ID")
    telegram_id: int = Field(..., description="Telegram user ID")
    name: str = Field(..., description="User name")
    gender: str = Field(..., description="User gender (male/female)")
    birth_date: date = Field(..., description="Birth date")
    birth_city: str = Field(..., description="Birth city")

    model_config = {"from_attributes": True}
