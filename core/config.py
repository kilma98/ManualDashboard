from __future__ import annotations
import os
from functools import lru_cache
from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ManualDashboard API"
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    database_url: AnyUrl
    vite_api_url: str = "http://localhost:5173"

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expires_minutes: int = 60 * 24

    cors_origins: str = "*"

    telegram_bot_token: str = "7607021778:AAE1aQegpTE1cwtOpXyLeR1lQk9kZIdFBKI" 
    telegram_admin_chat_id: str = "7608583110" 

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


