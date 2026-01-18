from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    model_config = {"env_file": ".env", "extra": "ignore"}
    
    # JWT Settings
    jwt_secret_key: str
    environment: str = "development"
    
    # Database Settings
    database_url: str = "sqlite://db.sqlite3"
    
    # Token Settings
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 3

    @property
    def cors_origins(self) -> str:
        """Get CORS origins from environment or default"""
        import os
        return os.getenv("CORS_ALLOWED_ORIGINS", "")


# Global settings instance
settings = Settings()