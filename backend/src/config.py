"""Environment configuration management."""

import os
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database - Railway auto-injects DATABASE_URL
    database_url: str = os.environ.get("DATABASE_URL", "sqlite:///./todo.db")

    # Logging
    log_level: str = "INFO"

    # CORS - comma-separated origins
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    # Server
    port: int = int(os.environ.get("PORT", "8000"))
    host: str = "0.0.0.0"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        origins = [origin.strip() for origin in self.cors_origins.split(",")]
        return [o for o in origins if o]  # Filter empty strings

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra env vars


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
