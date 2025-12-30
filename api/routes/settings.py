from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.database import get_session
from database.models import Setting
from typing import List
from pydantic import BaseModel


class SettingResponse(BaseModel):
    id: int
    key: str
    value: str
    description: str | None
    
    class Config:
        from_attributes = True


class SettingCreate(BaseModel):
    key: str
    value: str
    description: str | None = None


class SettingUpdate(BaseModel):
    value: str
    description: str | None = None


router = APIRouter(prefix="/settings", tags=["Settings"])


@router.get("/", response_model=List[SettingResponse])
async def get_settings(session: AsyncSession = Depends(get_session)):
    """Get all settings"""
    result = await session.execute(select(Setting))
    settings = result.scalars().all()
    return settings


@router.get("/{setting_id}", response_model=SettingResponse)
async def get_setting(
    setting_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get setting by ID"""
    result = await session.execute(
        select(Setting).where(Setting.id == setting_id)
    )
    setting = result.scalar_one_or_none()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting


@router.post("/", response_model=SettingResponse)
async def create_setting(
    setting: SettingCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create new setting"""
    new_setting = Setting(**setting.dict())
    session.add(new_setting)
    await session.commit()
    await session.refresh(new_setting)
    return new_setting


@router.put("/{setting_id}", response_model=SettingResponse)
async def update_setting(
    setting_id: int,
    setting_update: SettingUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update setting"""
    result = await session.execute(
        select(Setting).where(Setting.id == setting_id)
    )
    setting = result.scalar_one_or_none()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    
    setting.value = setting_update.value
    if setting_update.description is not None:
        setting.description = setting_update.description
    
    await session.commit()
    await session.refresh(setting)
    return setting


@router.delete("/{setting_id}")
async def delete_setting(
    setting_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Delete setting"""
    result = await session.execute(
        select(Setting).where(Setting.id == setting_id)
    )
    setting = result.scalar_one_or_none()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    
    await session.delete(setting)
    await session.commit()
    return {"message": "Setting deleted successfully"}
