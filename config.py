from pydantic_settings import BaseSettings
from typing import List
from pydantic import field_validator


class Settings(BaseSettings):
    # Telegram Bot
    BOT_TOKEN: str = ""
    ADMIN_IDS: str = ""
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./bot_database.db"
    
    @field_validator('DATABASE_URL')
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate that SQLite databases use async driver"""
        if v.startswith('sqlite:') and not v.startswith('sqlite+aiosqlite:'):
            raise ValueError(
                f"Invalid DATABASE_URL: '{v}'. "
                "SQLite databases must use the aiosqlite async driver. "
                "Please use 'sqlite+aiosqlite:///' instead of 'sqlite:///'.\n"
                "Example: DATABASE_URL=sqlite+aiosqlite:///./bot_database.db"
            )
        return v
    
    # FastAPI Admin Panel
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    SECRET_KEY: str = "change-this-secret-key-in-production"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"
    
    # Video Processing
    MAX_VIDEO_SIZE_MB: int = 100
    TEMP_VIDEO_DIR: str = "./temp_videos"
    PROCESSED_VIDEO_DIR: str = "./processed_videos"
    MAX_CARTESIAN_COMBINATIONS: int = 100  # Limit for all-with-all strategy in Mode N
    
    class Config:
        env_file = ".env"
        extra = "allow"
    
    def get_admin_ids(self) -> List[int]:
        if not self.ADMIN_IDS:
            return []
        return [int(id.strip()) for id in self.ADMIN_IDS.split(",") if id.strip()]


settings = Settings()
