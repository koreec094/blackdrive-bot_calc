from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bot_token: str = Field(alias="BOT_TOKEN")
    manager_telegram_url: str = Field(default="https://t.me/blackdriveauto1", alias="MANAGER_TELEGRAM_URL")
    korea_expenses_krw: int = Field(default=1_640_000, alias="KOREA_EXPENSES_KRW")
    encar_request_timeout: int = Field(default=15, alias="ENCAR_REQUEST_TIMEOUT")

    calculator_api_url: str | None = Field(default=None, alias="CALCULATOR_API_URL")
    calculator_api_token: str | None = Field(default=None, alias="CALCULATOR_API_TOKEN")


settings = Settings()
