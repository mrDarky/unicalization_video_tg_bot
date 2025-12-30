import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import settings
from database.database import init_db
from bot.handlers import basic, video_processing, mode2
from bot.states import VideoProcessingStates

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main bot function"""
    # Initialize bot and dispatcher
    bot = Bot(token=settings.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Initialize database
    logger.info("Initializing database...")
    await init_db()
    logger.info("Database initialized successfully")
    
    # Register routers
    dp.include_router(basic.router)
    dp.include_router(video_processing.router)
    dp.include_router(mode2.router)
    
    # Start polling
    logger.info("Bot started successfully")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
