"""
DEPRECATED: This script is no longer needed!

Migration is now automatic. The language column is automatically added
to existing databases when you run the bot or API server.

This script is kept for reference only.

---

Migration script to add language column to existing users table.
Run this script if you have an existing database.
"""
import asyncio
from sqlalchemy import text
from database.database import async_session_maker, engine


async def migrate_language_column():
    """Add language column to users table if it doesn't exist"""
    async with engine.begin() as conn:
        # Check if column exists
        result = await conn.execute(text(
            "SELECT COUNT(*) FROM pragma_table_info('users') WHERE name='language'"
        ))
        column_exists = result.scalar() > 0
        
        if not column_exists:
            print("Adding 'language' column to users table...")
            await conn.execute(text(
                "ALTER TABLE users ADD COLUMN language VARCHAR DEFAULT 'en' NOT NULL"
            ))
            print("✅ Language column added successfully!")
        else:
            print("✅ Language column already exists.")
    
    # Update any NULL values to 'en'
    async with async_session_maker() as session:
        await session.execute(text(
            "UPDATE users SET language = 'en' WHERE language IS NULL"
        ))
        await session.commit()
        print("✅ All users have language preference set.")


if __name__ == "__main__":
    print("Starting language column migration...")
    asyncio.run(migrate_language_column())
    print("Migration completed!")
