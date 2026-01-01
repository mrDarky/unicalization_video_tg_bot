from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload
from database.models import User, Video, Deposit, Withdrawal, Setting, Statistic
from datetime import datetime
from typing import Optional, List


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> Optional[User]:
    """Get user by telegram ID"""
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, telegram_id: int, username: str = None, 
                     first_name: str = None, last_name: str = None, referrer_id: int = None) -> User:
    """Create new user"""
    user = User(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        referrer_id=referrer_id
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_or_create_user(session: AsyncSession, telegram_id: int, username: str = None,
                             first_name: str = None, last_name: str = None) -> User:
    """Get existing user or create new one"""
    user = await get_user_by_telegram_id(session, telegram_id)
    if not user:
        user = await create_user(session, telegram_id, username, first_name, last_name)
    return user


async def get_user_with_referrals(session: AsyncSession, telegram_id: int) -> Optional[User]:
    """Get user by telegram ID with referrals eagerly loaded"""
    result = await session.execute(
        select(User)
        .where(User.telegram_id == telegram_id)
        .options(selectinload(User.referrals))
    )
    return result.scalar_one_or_none()


async def get_user_referrals_count(session: AsyncSession, user_id: int) -> int:
    """Get count of referrals for a user"""
    result = await session.execute(
        select(func.count(User.id)).where(User.referrer_id == user_id)
    )
    return result.scalar() or 0


async def update_user_language(session: AsyncSession, telegram_id: int, language: str):
    """Update user's language preference"""
    await session.execute(
        update(User).where(User.telegram_id == telegram_id).values(language=language)
    )
    await session.commit()


async def create_video(session: AsyncSession, user_id: int, file_id: str, mode: int,
                       original_filename: str = None) -> Video:
    """Create video record"""
    video = Video(
        user_id=user_id,
        file_id=file_id,
        mode=mode,
        original_filename=original_filename
    )
    session.add(video)
    await session.commit()
    await session.refresh(video)
    return video


async def update_video_status(session: AsyncSession, video_id: int, status: str,
                              processed_filename: str = None, modifications: str = None):
    """Update video processing status"""
    update_data = {"status": status}
    if status == "completed":
        update_data["processed_at"] = datetime.utcnow()
    if processed_filename:
        update_data["processed_filename"] = processed_filename
    if modifications:
        update_data["modifications"] = modifications
    
    await session.execute(
        update(Video).where(Video.id == video_id).values(**update_data)
    )
    await session.commit()


async def get_all_users(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    """Get all users with pagination"""
    result = await session.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def get_all_videos(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Video]:
    """Get all videos with pagination"""
    result = await session.execute(select(Video).offset(skip).limit(limit))
    return result.scalars().all()


async def get_user_videos(session: AsyncSession, user_id: int) -> List[Video]:
    """Get all videos for a user"""
    result = await session.execute(select(Video).where(Video.user_id == user_id))
    return result.scalars().all()


async def create_deposit(session: AsyncSession, user_id: int, amount: float,
                        payment_method: str = None) -> Deposit:
    """Create deposit record"""
    deposit = Deposit(
        user_id=user_id,
        amount=amount,
        payment_method=payment_method
    )
    session.add(deposit)
    await session.commit()
    await session.refresh(deposit)
    return deposit


async def create_withdrawal(session: AsyncSession, user_id: int, amount: float,
                           payment_method: str = None, wallet_address: str = None) -> Withdrawal:
    """Create withdrawal record"""
    withdrawal = Withdrawal(
        user_id=user_id,
        amount=amount,
        payment_method=payment_method,
        wallet_address=wallet_address
    )
    session.add(withdrawal)
    await session.commit()
    await session.refresh(withdrawal)
    return withdrawal


async def get_setting(session: AsyncSession, key: str) -> Optional[Setting]:
    """Get setting by key"""
    result = await session.execute(select(Setting).where(Setting.key == key))
    return result.scalar_one_or_none()


async def set_setting(session: AsyncSession, key: str, value: str, description: str = None):
    """Set or update setting"""
    setting = await get_setting(session, key)
    if setting:
        await session.execute(
            update(Setting).where(Setting.key == key).values(value=value, updated_at=datetime.utcnow())
        )
    else:
        setting = Setting(key=key, value=value, description=description)
        session.add(setting)
    await session.commit()


async def get_statistics(session: AsyncSession) -> dict:
    """Get overall statistics"""
    total_users = await session.execute(select(func.count(User.id)))
    active_users = await session.execute(select(func.count(User.id)).where(User.is_active == True))
    total_videos = await session.execute(select(func.count(Video.id)))
    processed_videos = await session.execute(
        select(func.count(Video.id)).where(Video.status == "completed")
    )
    
    return {
        "total_users": total_users.scalar(),
        "active_users": active_users.scalar(),
        "total_videos": total_videos.scalar(),
        "processed_videos": processed_videos.scalar()
    }
