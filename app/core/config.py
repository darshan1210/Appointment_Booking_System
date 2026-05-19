from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    
    PROJECT_NAME: str
    DATABASE_URL: str
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    JWT_SECRET_KEY :str
    JWT_ALGO :str
    
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    REFRESH_TOKEN_EXPIRE_DAYS:int
    
    SUPER_ADMIN_SECRET :str
    
    API_V1_STR:str
    ENVIRONMENT: str 
    DEBUG: bool
    
@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()  # pyright: ignore[reportCallIssue]