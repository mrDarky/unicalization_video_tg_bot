from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database.database import get_session
from database.models import Video
from typing import List
from pydantic import BaseModel
from datetime import datetime


class VideoResponse(BaseModel):
    id: int
    user_id: int
    file_id: str
    original_filename: str | None
    processed_filename: str | None
    mode: int
    status: str
    created_at: datetime
    processed_at: datetime | None
    
    class Config:
        from_attributes = True


class VideoUpdate(BaseModel):
    status: str | None = None


router = APIRouter(prefix="/videos", tags=["Videos"])


@router.get("/", response_model=List[VideoResponse])
async def get_videos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: str | None = None,
    session: AsyncSession = Depends(get_session)
):
    """Get all videos"""
    query = select(Video)
    if status:
        query = query.where(Video.status == status)
    
    result = await session.execute(
        query.offset(skip).limit(limit)
    )
    videos = result.scalars().all()
    return videos


@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(
    video_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get video by ID"""
    result = await session.execute(
        select(Video).where(Video.id == video_id)
    )
    video = result.scalar_one_or_none()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


@router.put("/{video_id}", response_model=VideoResponse)
async def update_video(
    video_id: int,
    video_update: VideoUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update video"""
    result = await session.execute(
        select(Video).where(Video.id == video_id)
    )
    video = result.scalar_one_or_none()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    if video_update.status:
        video.status = video_update.status
    
    await session.commit()
    await session.refresh(video)
    return video


@router.delete("/{video_id}")
async def delete_video(
    video_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Delete video"""
    result = await session.execute(
        select(Video).where(Video.id == video_id)
    )
    video = result.scalar_one_or_none()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    await session.delete(video)
    await session.commit()
    return {"message": "Video deleted successfully"}


@router.get("/stats/count")
async def get_videos_count(session: AsyncSession = Depends(get_session)):
    """Get videos statistics"""
    total = await session.execute(select(func.count(Video.id)))
    completed = await session.execute(
        select(func.count(Video.id)).where(Video.status == "completed")
    )
    pending = await session.execute(
        select(func.count(Video.id)).where(Video.status == "pending")
    )
    
    return {
        "total_videos": total.scalar(),
        "completed_videos": completed.scalar(),
        "pending_videos": pending.scalar()
    }
