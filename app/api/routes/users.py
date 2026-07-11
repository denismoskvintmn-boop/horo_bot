from fastapi import APIRouter, Depends, HTTPException, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api.schemas import UserResponse
from app.core.config import settings
from app.database.database import async_session_factory
from app.services.user_service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["users"])

limiter = Limiter(key_func=get_remote_address)


@router.get("/{telegram_id}", response_model=UserResponse)
@limiter.limit("30/minute")
async def get_user(
    request: Request,
    telegram_id: int,
) -> UserResponse:
    async with async_session_factory() as session:
        user_service = UserService(session)
        try:
            user = await user_service.get_user_by_telegram_id(telegram_id)
            return UserResponse(
                id=user.id,
                telegram_id=user.telegram_id,
                name=user.name,
                gender=user.gender,
                birth_date=user.birth_date,
                birth_city=user.birth_city,
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
