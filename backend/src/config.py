"""Environment configuration management."""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        database_url: PostgreSQL connection string (required)
        log_level: Logging level (default: INFO)
        cors_origins: Allowed CORS origins (default: localhost:3000)
    """

    database_url: str = "sqlite:///./todo.db"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
