from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api.schemas import HoroscopeNotFoundResponse, HoroscopeResponse
from app.database.database import async_session_factory
from app.database.repositories.horoscope_repository import HoroscopeRepository
from app.services.user_service import UserService

router = APIRouter(prefix="/api/v1/horoscopes", tags=["horoscopes"])

limiter = Limiter(key_func=get_remote_address)


@router.get(
    "/{telegram_id}",
    response_model=HoroscopeResponse | HoroscopeNotFoundResponse,
)
@limiter.limit("10/minute")
async def get_horoscope(
    request: Request,
    telegram_id: int,
) -> HoroscopeResponse | HoroscopeNotFoundResponse:
    async with async_session_factory() as session:
        user_service = UserService(session)
        try:
            user = await user_service.get_user_by_telegram_id(telegram_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        repo = HoroscopeRepository(session)
        horoscope = await repo.get_by_user_and_date(user.id, date.today())

        if not horoscope:
            return HoroscopeNotFoundResponse(info="No horoscope for today")

        return HoroscopeResponse(
            date=horoscope.date,
            text=horoscope.text,
            status=horoscope.status,
        )
