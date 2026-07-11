import logging

from fastapi import FastAPI, Request
from fastapi.security import APIKeyHeader
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.routes import health_router, horoscopes_router, users_router
from app.core.config import settings

logger = logging.getLogger(__name__)

app = FastAPI(title="Horoscope API", version="1.0.0")

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# API key security
API_KEY = settings.API_SECRET_KEY.get_secret_value()
api_key_header = APIKeyHeader(name="X-API-Key")


# Include routers
app.include_router(health_router)
app.include_router(users_router)
app.include_router(horoscopes_router)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> None:
    from fastapi import HTTPException, status

    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail="Rate limit exceeded",
    )
