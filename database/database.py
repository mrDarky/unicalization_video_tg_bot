from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from database.models import Base
from config import settings
import os
import logging

logger = logging.getLogger(__name__)

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True
)

# Create async session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    """Initialize database and create all tables"""
    # Create directories for videos
    os.makedirs(settings.TEMP_VIDEO_DIR, exist_ok=True)
    os.makedirs(settings.PROCESSED_VIDEO_DIR, exist_ok=True)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        # Migration: Add language column to users table if it doesn't exist
        # This handles existing databases that were created before the language feature
        try:
            result = await conn.execute(text(
                "SELECT COUNT(*) FROM pragma_table_info('users') WHERE name='language'"
            ))
            column_exists = result.scalar() > 0
            
            if not column_exists:
                logger.info("Adding 'language' column to users table...")
                await conn.execute(text(
                    "ALTER TABLE users ADD COLUMN language VARCHAR DEFAULT 'en' NOT NULL"
                ))
                logger.info("✅ Language column added successfully!")
            else:
                logger.debug("Language column already exists in users table")
        except Exception as e:
            logger.warning(f"Could not check/add language column (may not be SQLite): {e}")
    
    # Update any NULL values to 'en' (for safety)
    try:
        async with async_session_maker() as session:
            await session.execute(text(
                "UPDATE users SET language = 'en' WHERE language IS NULL OR language = ''"
            ))
            await session.commit()
            logger.debug("Ensured all users have language preference set")
    except Exception as e:
        logger.warning(f"Could not update NULL language values: {e}")


async def get_session() -> AsyncSession:
    """Get database session"""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
