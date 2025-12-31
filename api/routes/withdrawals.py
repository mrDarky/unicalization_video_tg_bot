from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.database import get_session
from database.models import Withdrawal
from typing import List
from pydantic import BaseModel
from datetime import datetime


class WithdrawalResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    status: str
    payment_method: str | None
    wallet_address: str | None
    created_at: datetime
    completed_at: datetime | None
    
    class Config:
        from_attributes = True


class WithdrawalCreate(BaseModel):
    user_id: int
    amount: float
    payment_method: str | None = None
    wallet_address: str | None = None


class WithdrawalUpdate(BaseModel):
    status: str | None = None


router = APIRouter(prefix="/withdrawals", tags=["Withdrawals"])


@router.get("/", response_model=List[WithdrawalResponse])
async def get_withdrawals(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: str | None = None,
    session: AsyncSession = Depends(get_session)
):
    """Get all withdrawals"""
    query = select(Withdrawal)
    if status:
        query = query.where(Withdrawal.status == status)
    
    result = await session.execute(
        query.offset(skip).limit(limit)
    )
    withdrawals = result.scalars().all()
    return withdrawals


@router.get("/{withdrawal_id}", response_model=WithdrawalResponse)
async def get_withdrawal(
    withdrawal_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get withdrawal by ID"""
    result = await session.execute(
        select(Withdrawal).where(Withdrawal.id == withdrawal_id)
    )
    withdrawal = result.scalar_one_or_none()
    if not withdrawal:
        raise HTTPException(status_code=404, detail="Withdrawal not found")
    return withdrawal


@router.post("/", response_model=WithdrawalResponse)
async def create_withdrawal(
    withdrawal: WithdrawalCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create new withdrawal"""
    new_withdrawal = Withdrawal(**withdrawal.dict())
    session.add(new_withdrawal)
    await session.commit()
    await session.refresh(new_withdrawal)
    return new_withdrawal


@router.put("/{withdrawal_id}", response_model=WithdrawalResponse)
async def update_withdrawal(
    withdrawal_id: int,
    withdrawal_update: WithdrawalUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update withdrawal"""
    result = await session.execute(
        select(Withdrawal).where(Withdrawal.id == withdrawal_id)
    )
    withdrawal = result.scalar_one_or_none()
    if not withdrawal:
        raise HTTPException(status_code=404, detail="Withdrawal not found")
    
    if withdrawal_update.status:
        withdrawal.status = withdrawal_update.status
        if withdrawal_update.status == "completed":
            withdrawal.completed_at = datetime.utcnow()
    
    await session.commit()
    await session.refresh(withdrawal)
    return withdrawal


@router.delete("/{withdrawal_id}")
async def delete_withdrawal(
    withdrawal_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Delete withdrawal"""
    result = await session.execute(
        select(Withdrawal).where(Withdrawal.id == withdrawal_id)
    )
    withdrawal = result.scalar_one_or_none()
    if not withdrawal:
        raise HTTPException(status_code=404, detail="Withdrawal not found")
    
    await session.delete(withdrawal)
    await session.commit()
    return {"message": "Withdrawal deleted successfully"}
