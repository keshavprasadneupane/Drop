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

Log.info(f"Settings loaded: DEBUG={settings.DEBUG}, DATABASE_URL={settings.DATABASE_URL}, SECRET_KEY={settings.SECRET_KEY}, REFRESH_SECRET_KEY={settings.REFRESH_SECRET_KEY}, ALGORITHM={settings.ALGORITHM}, ACCESS_TOKEN_EXPIRE_MINUTES={settings.ACCESS_TOKEN_EXPIRE_MINUTES}, REFRESH_TOKEN_EXPIRE_DAYS={settings.REFRESH_TOKEN_EXPIRE_DAYS}")