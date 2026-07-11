from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Telegram
    TELEGRAM_BOT_TOKEN: SecretStr = Field(..., description="Токен Telegram бота")

    # DeepSeek
    DEEPSEEK_API_KEY: SecretStr = Field(..., description="Ключ DeepSeek API")
    DEEPSEEK_API_URL: str = Field(
        default="https://api.deepseek.com/v1/chat/completions",
        description="URL DeepSeek API",
    )

    # Database
    DATABASE_URL: str = Field(..., description="Строка подключения к PostgreSQL")

    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0", description="URL Redis")

    # Swiss Ephemeris
    SWISSEPH_PATH: str = Field(default="/usr/share/swisseph", description="Путь к файлам эфемерид")

    # Scheduler
    HOROSCOPE_SEND_TIME: str = Field(default="07:00", description="Время рассылки (HH:MM)")
    TIMEZONE: str = Field(default="UTC", description="Часовой пояс")

    # API Security
    API_SECRET_KEY: SecretStr = Field(..., description="Секретный ключ для API")

    # Sentry
    SENTRY_DSN: str | None = Field(default=None, description="DSN для Sentry")

    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Уровень логирования")


settings = Settings()
