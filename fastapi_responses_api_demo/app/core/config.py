from functools import lru_cache
from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-5-nano-2025-08-07"
    openai_max_output_tokens: int = 512
    database_url: str = "sqlite:///./responses_chat.db"
    environment: Literal["development",
                         "production", "testing"] = "development"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
