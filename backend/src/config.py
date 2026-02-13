"""Environment configuration management."""

# Task T045: Add Dapr Pub/Sub config settings (DAPR_HTTP_PORT, PUBSUB_NAME)
# Task T062: Add optional Dapr Secrets retrieval for DATABASE_URL and OPENAI_API_KEY

import os
from functools import lru_cache
from typing import List, Optional

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

    # OpenAI API Key for ChatKit
    openai_api_key: str = ""

    # Dapr Pub/Sub configuration (T045)
    dapr_http_port: int = int(os.environ.get("DAPR_HTTP_PORT", "3500"))
    pubsub_name: str = os.environ.get("PUBSUB_NAME", "kafka-pubsub")

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


# Task T062: Optional Dapr Secrets retrieval
async def get_secret_from_dapr(secret_name: str, dapr_port: int = 3500) -> Optional[str]:
    """Retrieve a secret from Dapr Secrets API.

    Falls back to None if Dapr is not available or the secret doesn't exist.
    Use this for production Kubernetes environments where secrets are managed via K8s Secrets.

    Args:
        secret_name: Name of the secret in Kubernetes (e.g., "database-url", "openai-api-key")
        dapr_port: Dapr sidecar HTTP port (default: 3500)

    Returns:
        Secret value if found, None otherwise
    """
    import httpx

    url = f"http://localhost:{dapr_port}/v1.0/secrets/kubernetes-secrets/{secret_name}"

    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(url)
            if response.status_code == 200:
                secrets_dict = response.json()
                # Kubernetes secrets store returns a dict with the secret name as key
                # Try both the secret name and common keys
                return secrets_dict.get(secret_name) or secrets_dict.get("value") or next(iter(secrets_dict.values()), None)
            elif response.status_code == 404:
                return None
            else:
                return None
    except Exception:
        # Dapr not available or other error - graceful degradation
        return None


def get_database_url_with_dapr_fallback() -> str:
    """Get DATABASE_URL from env var or Dapr Secrets API.

    Priority:
    1. Environment variable DATABASE_URL (for local dev and Railway)
    2. Dapr Secrets API (for Kubernetes deployments)
    3. Default SQLite fallback

    Returns:
        Database connection URL
    """
    # First check env var (works for Railway and local dev)
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        return db_url

    # Try Dapr Secrets API (synchronous wrapper)
    try:
        import asyncio
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Can't use asyncio.run in a running loop - skip Dapr lookup
            pass
        else:
            dapr_secret = asyncio.run(get_secret_from_dapr("database-url"))
            if dapr_secret:
                return dapr_secret
    except Exception:
        pass

    # Fallback to SQLite
    return "sqlite:///./todo.db"


def get_openai_api_key_with_dapr_fallback() -> str:
    """Get OPENAI_API_KEY from env var or Dapr Secrets API.

    Priority:
    1. Environment variable OPENAI_API_KEY (for local dev)
    2. Dapr Secrets API (for Kubernetes deployments)
    3. Empty string (chatbot will be disabled)

    Returns:
        OpenAI API key or empty string
    """
    # First check env var
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if api_key:
        return api_key

    # Try Dapr Secrets API (synchronous wrapper)
    try:
        import asyncio
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Can't use asyncio.run in a running loop - skip Dapr lookup
            pass
        else:
            dapr_secret = asyncio.run(get_secret_from_dapr("openai-api-key"))
            if dapr_secret:
                return dapr_secret
    except Exception:
        pass

    # Return empty string - chatbot will be disabled
    return ""


settings = get_settings()
