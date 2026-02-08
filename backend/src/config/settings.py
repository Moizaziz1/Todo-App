from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from pathlib import Path


# Get the backend directory path
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    JWT secret must match BETTER_AUTH_SECRET in the frontend.
    """
    model_config = SettingsConfigDict(
        env_file=str(BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    app_name: str = "Task Management API"
    app_version: str = "1.0.0"
    debug: bool = False

    # Database settings
    database_url: str = "postgresql://user:password@localhost/taskdb"

    # JWT settings - MUST match Better Auth configuration in frontend
    secret_key: str = "your-secret-key-here"  # Must match BETTER_AUTH_SECRET
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours to match Better Auth

    # CORS settings - allow frontend origin
    allowed_origins: str = "http://localhost:3000"

    @property
    def cors_origins(self) -> List[str]:
        """Parse allowed origins into a list."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


# Create a single instance of settings
settings = Settings()
settings = Settings()