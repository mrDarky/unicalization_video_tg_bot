from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database.database import get_session
from database.models import Deposit
from typing import List
from pydantic import BaseModel
from datetime import datetime


class DepositResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    status: str
    payment_method: str | None
    transaction_id: str | None
    created_at: datetime
    completed_at: datetime | None
    
    class Config:
        from_attributes = True


class DepositCreate(BaseModel):
    user_id: int
    amount: float
    payment_method: str | None = None


class DepositUpdate(BaseModel):
    status: str | None = None
    transaction_id: str | None = None


router = APIRouter(prefix="/deposits", tags=["Deposits"])


@router.get("/", response_model=List[DepositResponse])
async def get_deposits(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: str | None = None,
    session: AsyncSession = Depends(get_session)
):
    """Get all deposits"""
    query = select(Deposit)
    if status:
        query = query.where(Deposit.status == status)
    
    result = await session.execute(
        query.offset(skip).limit(limit)
    )
    deposits = result.scalars().all()
    return deposits


@router.get("/{deposit_id}", response_model=DepositResponse)
async def get_deposit(
    deposit_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get deposit by ID"""
    result = await session.execute(
        select(Deposit).where(Deposit.id == deposit_id)
    )
    deposit = result.scalar_one_or_none()
    if not deposit:
        raise HTTPException(status_code=404, detail="Deposit not found")
    return deposit


@router.post("/", response_model=DepositResponse)
async def create_deposit(
    deposit: DepositCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create new deposit"""
    new_deposit = Deposit(**deposit.dict())
    session.add(new_deposit)
    await session.commit()
    await session.refresh(new_deposit)
    return new_deposit


@router.put("/{deposit_id}", response_model=DepositResponse)
async def update_deposit(
    deposit_id: int,
    deposit_update: DepositUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update deposit"""
    result = await session.execute(
        select(Deposit).where(Deposit.id == deposit_id)
    )
    deposit = result.scalar_one_or_none()
    if not deposit:
        raise HTTPException(status_code=404, detail="Deposit not found")
    
    if deposit_update.status:
        deposit.status = deposit_update.status
        if deposit_update.status == "completed":
            deposit.completed_at = datetime.utcnow()
    if deposit_update.transaction_id:
        deposit.transaction_id = deposit_update.transaction_id
    
    await session.commit()
    await session.refresh(deposit)
    return deposit


@router.delete("/{deposit_id}")
async def delete_deposit(
    deposit_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Delete deposit"""
    result = await session.execute(
        select(Deposit).where(Deposit.id == deposit_id)
    )
    deposit = result.scalar_one_or_none()
    if not deposit:
        raise HTTPException(status_code=404, detail="Deposit not found")
    
    await session.delete(deposit)
    await session.commit()
    return {"message": "Deposit deleted successfully"}
