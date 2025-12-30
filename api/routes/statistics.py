from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database.database import get_session
from database.models import User, Video, Deposit, Withdrawal
from pydantic import BaseModel


class StatisticsResponse(BaseModel):
    total_users: int
    active_users: int
    total_videos: int
    completed_videos: int
    pending_videos: int
    processing_videos: int
    failed_videos: int
    total_deposits: float
    total_withdrawals: float
    pending_deposits: int
    pending_withdrawals: int


router = APIRouter(prefix="/statistics", tags=["Statistics"])


@router.get("/", response_model=StatisticsResponse)
async def get_statistics(session: AsyncSession = Depends(get_session)):
    """Get overall statistics"""
    # Users stats
    total_users = await session.execute(select(func.count(User.id)))
    active_users = await session.execute(
        select(func.count(User.id)).where(User.is_active == True)
    )
    
    # Videos stats
    total_videos = await session.execute(select(func.count(Video.id)))
    completed_videos = await session.execute(
        select(func.count(Video.id)).where(Video.status == "completed")
    )
    pending_videos = await session.execute(
        select(func.count(Video.id)).where(Video.status == "pending")
    )
    processing_videos = await session.execute(
        select(func.count(Video.id)).where(Video.status == "processing")
    )
    failed_videos = await session.execute(
        select(func.count(Video.id)).where(Video.status == "failed")
    )
    
    # Deposits stats
    total_deposits = await session.execute(
        select(func.sum(Deposit.amount)).where(Deposit.status == "completed")
    )
    pending_deposits = await session.execute(
        select(func.count(Deposit.id)).where(Deposit.status == "pending")
    )
    
    # Withdrawals stats
    total_withdrawals = await session.execute(
        select(func.sum(Withdrawal.amount)).where(Withdrawal.status == "completed")
    )
    pending_withdrawals = await session.execute(
        select(func.count(Withdrawal.id)).where(Withdrawal.status == "pending")
    )
    
    return StatisticsResponse(
        total_users=total_users.scalar() or 0,
        active_users=active_users.scalar() or 0,
        total_videos=total_videos.scalar() or 0,
        completed_videos=completed_videos.scalar() or 0,
        pending_videos=pending_videos.scalar() or 0,
        processing_videos=processing_videos.scalar() or 0,
        failed_videos=failed_videos.scalar() or 0,
        total_deposits=total_deposits.scalar() or 0.0,
        total_withdrawals=total_withdrawals.scalar() or 0.0,
        pending_deposits=pending_deposits.scalar() or 0,
        pending_withdrawals=pending_withdrawals.scalar() or 0
    )
