from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.database import get_session
from database.models import TariffPlan
from database.crud import (
    get_all_tariff_plans, 
    get_tariff_plan, 
    create_tariff_plan,
    update_tariff_plan,
    delete_tariff_plan,
    assign_tariff_plan_to_user
)
from typing import List
from pydantic import BaseModel


class TariffPlanResponse(BaseModel):
    id: int
    name: str
    description: str | None
    videos_per_day: int
    videos_per_order: int
    price: float
    is_active: bool
    
    class Config:
        from_attributes = True


class TariffPlanCreate(BaseModel):
    name: str
    description: str | None = None
    videos_per_day: int = 10
    videos_per_order: int = 5
    price: float = 0.0


class TariffPlanUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    videos_per_day: int | None = None
    videos_per_order: int | None = None
    price: float | None = None
    is_active: bool | None = None


class UserTariffAssignment(BaseModel):
    user_id: int
    tariff_plan_id: int


router = APIRouter(prefix="/tariff-plans", tags=["Tariff Plans"])


@router.get("/", response_model=List[TariffPlanResponse])
async def get_tariff_plans(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    """Get all tariff plans"""
    plans = await get_all_tariff_plans(session, skip, limit)
    return plans


@router.get("/{plan_id}", response_model=TariffPlanResponse)
async def get_plan(
    plan_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get tariff plan by ID"""
    plan = await get_tariff_plan(session, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Tariff plan not found")
    return plan


@router.post("/", response_model=TariffPlanResponse)
async def create_plan(
    plan_data: TariffPlanCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create new tariff plan"""
    plan = await create_tariff_plan(
        session,
        name=plan_data.name,
        description=plan_data.description,
        videos_per_day=plan_data.videos_per_day,
        videos_per_order=plan_data.videos_per_order,
        price=plan_data.price
    )
    return plan


@router.put("/{plan_id}", response_model=TariffPlanResponse)
async def update_plan(
    plan_id: int,
    plan_update: TariffPlanUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update tariff plan"""
    plan = await get_tariff_plan(session, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Tariff plan not found")
    
    update_data = {k: v for k, v in plan_update.dict().items() if v is not None}
    if update_data:
        await update_tariff_plan(session, plan_id, **update_data)
    
    # Fetch updated plan
    plan = await get_tariff_plan(session, plan_id)
    return plan


@router.delete("/{plan_id}")
async def delete_plan(
    plan_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Delete tariff plan"""
    plan = await get_tariff_plan(session, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Tariff plan not found")
    
    await delete_tariff_plan(session, plan_id)
    return {"message": "Tariff plan deleted successfully"}


@router.post("/assign")
async def assign_plan_to_user(
    assignment: UserTariffAssignment,
    session: AsyncSession = Depends(get_session)
):
    """Assign tariff plan to user"""
    await assign_tariff_plan_to_user(session, assignment.user_id, assignment.tariff_plan_id)
    return {"message": "Tariff plan assigned successfully"}
