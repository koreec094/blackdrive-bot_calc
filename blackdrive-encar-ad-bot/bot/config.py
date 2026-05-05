from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bot_token: str = Field(alias="BOT_TOKEN")
    manager_telegram_url: str = Field(default="https://t.me/blackdriveauto1", alias="MANAGER_TELEGRAM_URL")
    korea_expenses_krw: int = Field(default=1_640_000, alias="KOREA_EXPENSES_KRW")
    encar_request_timeout: int = Field(default=15, alias="ENCAR_REQUEST_TIMEOUT")
    allowed_usernames: str = Field(default="", alias="ALLOWED_USERNAMES")

    @property
    def allowed_usernames_set(self) -> set[str]:
        return {username.strip().lower().lstrip("@") for username in self.allowed_usernames.split(",") if username.strip()}


settings = Settings()
