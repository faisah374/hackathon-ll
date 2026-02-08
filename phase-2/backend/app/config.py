"""Configuration module for Todo Backend API"""
import os
from typing import Optional
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # Authentication settings
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET")
    NEXT_PUBLIC_BETTER_AUTH_URL: str = os.getenv("NEXT_PUBLIC_BETTER_AUTH_URL", "http://localhost:3000")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Application settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Todo Backend API"
    VERSION: str = "1.0.0"

    # Database settings
    DB_ECHO: bool = os.getenv("DB_ECHO", "False").lower() == "true"
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    DB_POOL_RECYCLE: int = int(os.getenv("DB_POOL_RECYCLE", "300"))  # 5 minutes
    DB_POOL_TIMEOUT: int = int(os.getenv("DB_POOL_TIMEOUT", "30"))  # 30 seconds

    class Config:
        env_file = ".env"


settings = Settings()