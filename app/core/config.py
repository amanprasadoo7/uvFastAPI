from typing import List
from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Database
    database_url: PostgresDsn = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/dbname"
    )
    
    # Application
    app_name: str = Field(default="FastAPI CRUD Service")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")
    
    # API
    api_v1_prefix: str = Field(default="/api/v1")
    allowed_origins: List[str] = Field(default=["http://localhost:3000"])
    
    # Server
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    workers: int = Field(default=4)
    
    # JWT Authentication
    secret_key: str = Field(..., min_length=32)
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    refresh_token_expire_days: int = Field(default=7)
    
    # Auth0
    auth0_domain: str = Field(default="")
    auth0_api_audience: str = Field(default="")
    auth0_issuer: str = Field(default="")
    auth0_algorithms: str = Field(default="RS256")
    
    # Google OAuth
    google_client_id: str = Field(default="")
    google_client_secret: str = Field(default="")
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0")
    
    # Email
    smtp_host: str = Field(default="smtp.gmail.com")
    smtp_port: int = Field(default=587)
    smtp_user: str = Field(default="")
    smtp_password: str = Field(default="")
    email_from: str = Field(default="")
    
    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = Settings()