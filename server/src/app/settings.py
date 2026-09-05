from app.core.logger import Log
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	DEBUG: bool = True
	# Database settings
	DATABASE_URL: str = "sqlite+aiosqlite:///./database.db"

	# Security settings, JWT settings
	SECRET_KEY: str = "your-secret-key"
	REFRESH_SECRET_KEY: str = "your-refresh-secret-key"
	ALGORITHM: str = "HS256"	

	# Token expiration settings
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
	REFRESH_TOKEN_EXPIRE_DAYS: int = 7

	model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore", 
    )
	
settings = Settings()