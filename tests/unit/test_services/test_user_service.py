from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.mark.asyncio
async def test_user_service_register():
    from datetime import date

    from app.services.user_service import UserService

    mock_db = AsyncMock()
    mock_repo = MagicMock()
    mock_repo.get_by_telegram_id = AsyncMock(return_value=None)
    mock_repo.create = AsyncMock(
        return_value=MagicMock(
            id=1,
            telegram_id=123456,
            name="Test",
            gender="male",
            birth_date=date(2000, 1, 1),
            birth_city="Moscow",
        )
    )

    with patch("app.services.user_service.UserRepository", return_value=mock_repo):
        service = UserService(mock_db)
        user = await service.register_user(
            telegram_id=123456,
            username="test_user",
            name="Test",
            gender="male",
            birth_date=date(2000, 1, 1),
            birth_city="Moscow",
        )
        assert user.name == "Test"
        assert user.telegram_id == 123456
