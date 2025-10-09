from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str
    database_url: str = "sqlite:///./chat_app.db"
    openai_model: str = "gpt-5-codex-preview"
    openai_temperature: float = 0.7
    openai_max_output_tokens: int = 512
    openai_fallback_model: str | None = "gpt-4o-mini"
    environment: Literal["development",
                         "production", "testing"] = "development"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
