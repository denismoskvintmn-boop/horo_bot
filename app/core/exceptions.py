class AppError(Exception):
    """Base exception for the application."""


class UserAlreadyExistsError(AppError):
    """Raised when trying to register an existing user."""


class UserNotFoundError(AppError):
    """Raised when a user is not found."""


class HoroscopeAlreadyExistsError(AppError):
    """Raised when a horoscope for the given date already exists."""


class HoroscopeNotFoundError(AppError):
    """Raised when a horoscope is not found."""


class DeepSeekAPIError(AppError):
    """Raised when DeepSeek API returns an error."""


class AstronomyCalculationError(AppError):
    """Raised when astronomical calculation fails."""


class InvalidInputError(AppError):
    """Raised when user input is invalid."""
