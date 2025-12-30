from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Telegram Bot
    BOT_TOKEN: str = ""
    ADMIN_IDS: str = ""
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./bot_database.db"
    
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
    
    class Config:
        env_file = ".env"
        extra = "allow"
    
    def get_admin_ids(self) -> List[int]:
        if not self.ADMIN_IDS:
            return []
        return [int(id.strip()) for id in self.ADMIN_IDS.split(",") if id.strip()]


settings = Settings()
