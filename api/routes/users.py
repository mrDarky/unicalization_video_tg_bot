from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database.database import get_session
from database.models import User
from typing import List
from pydantic import BaseModel
from datetime import datetime


class UserResponse(BaseModel):
    id: int
    telegram_id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    created_at: datetime
    is_active: bool
    balance: float
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    is_active: bool | None = None
    balance: float | None = None


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: AsyncSession = Depends(get_session)
):
    """Get all users"""
    result = await session.execute(
        select(User).offset(skip).limit(limit)
    )
    users = result.scalars().all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get user by ID"""
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update user"""
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.is_active is not None:
        user.is_active = user_update.is_active
    if user_update.balance is not None:
        user.balance = user_update.balance
    
    await session.commit()
    await session.refresh(user)
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Delete user"""
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await session.delete(user)
    await session.commit()
    return {"message": "User deleted successfully"}


@router.get("/stats/count")
async def get_users_count(session: AsyncSession = Depends(get_session)):
    """Get total users count"""
    result = await session.execute(select(func.count(User.id)))
    count = result.scalar()
    return {"total_users": count}
