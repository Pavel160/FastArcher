from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class BaseConfig(BaseSettings):
    """Конфигурация приложения.
    Настройки загружаются из файла `.env` и автоматически валидируются с помощью Pydantic.
    Содержит параметры для подключения к PostgreSQL, токен Telegram-бота и адрес API."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

class DBConfig(BaseConfig):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_INTERNAL_PORT: int
    DB_EXTERNAL_PORT: int

class APIConfig(BaseConfig):
    API_HOST: str
    API_INTERNAL_PORT: int
    API_EXTERNAL_PORT: int

class TELEGRAMConfig(BaseConfig):
    TELEGRAM_TOKEN: str


class Settings(BaseConfig):

    postgres: DBConfig = Field(default_factory=DBConfig)
    telegram: TELEGRAMConfig = Field(default_factory=TELEGRAMConfig)
    api: APIConfig = Field(default_factory=APIConfig)


settings = Settings()
