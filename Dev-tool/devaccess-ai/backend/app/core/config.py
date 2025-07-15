"""
Configuration settings for DevAccess AI
"""
from typing import List, Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "DevAccess AI"
    DEBUG: bool = Field(default=False, env="DEBUG")
    VERSION: str = "1.0.0"
    
    # API
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = Field(default="default-secret-key-change-in-production", env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS
    ALLOWED_HOSTS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        env="ALLOWED_HOSTS"
    )
    
    @validator("ALLOWED_HOSTS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    # Database
    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./devaccess_ai.db", env="DATABASE_URL")
    DATABASE_ECHO: bool = Field(default=False, env="DATABASE_ECHO")
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    
    # Celery
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/1", env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/2", env="CELERY_RESULT_BACKEND")
    
    # HashiCorp Vault
    VAULT_URL: Optional[str] = Field(default=None, env="VAULT_URL")
    VAULT_TOKEN: Optional[str] = Field(default=None, env="VAULT_TOKEN")
    VAULT_MOUNT_POINT: str = Field(default="secret", env="VAULT_MOUNT_POINT")
    
    # Email Services
    TEMP_EMAIL_PROVIDERS: List[str] = Field(
        default=[
            "https://api.mailinator.com",
            "https://api.guerrillamail.com",
            "https://temp-mail.org/api"
        ],
        env="TEMP_EMAIL_PROVIDERS"
    )
    
    # Web Automation
    SELENIUM_GRID_URL: Optional[str] = Field(default=None, env="SELENIUM_GRID_URL")
    PLAYWRIGHT_BROWSER_TYPE: str = Field(default="chromium", env="PLAYWRIGHT_BROWSER_TYPE")
    AUTOMATION_TIMEOUT: int = Field(default=30, env="AUTOMATION_TIMEOUT")
    AUTOMATION_HEADLESS: bool = Field(default=True, env="AUTOMATION_HEADLESS")
    
    # AI/NLP
    HUGGINGFACE_API_KEY: Optional[str] = Field(default=None, env="HUGGINGFACE_API_KEY")
    SPACY_MODEL: str = Field(default="en_core_web_sm", env="SPACY_MODEL")
    
    # CAPTCHA Services
    CAPTCHA_SERVICE_API_KEY: Optional[str] = Field(default=None, env="CAPTCHA_SERVICE_API_KEY")
    CAPTCHA_SERVICE_URL: Optional[str] = Field(default=None, env="CAPTCHA_SERVICE_URL")
    
    # Security
    ENCRYPTION_KEY: str = Field(default="default-encryption-key-change-in-production", env="ENCRYPTION_KEY")
    PASSWORD_MIN_LENGTH: int = Field(default=12, env="PASSWORD_MIN_LENGTH")
    PASSWORD_INCLUDE_SYMBOLS: bool = Field(default=True, env="PASSWORD_INCLUDE_SYMBOLS")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    RATE_LIMIT_PER_HOUR: int = Field(default=1000, env="RATE_LIMIT_PER_HOUR")
    
    # Monitoring
    SENTRY_DSN: Optional[str] = Field(default=None, env="SENTRY_DSN")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
