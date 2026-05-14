from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    PROJECT_NAME:str
    DATABASE_URL:str
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    
@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()  # pyright: ignore[reportCallIssue]