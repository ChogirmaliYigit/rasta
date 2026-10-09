from __future__ import annotations
from fastapi import APIRouter, Depends
from uuid import UUID
from app.dependencies import get_db
from app.dependencies import get_current_user, CurrentUser, RoleChecker
from app.schemas.return_act import ReturnActCreate, ReturnActResponse
from app.services import return_service
from sqlalchemy import select
from app.models.return_act import ReturnAct
from app.schemas.common import ReturnActStatus

router = APIRouter(prefix="/return-acts", tags=["return_acts"])

@router.post("/", response_model=ReturnActResponse)
async def create_return_act(data: ReturnActCreate, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(RoleChecker(["RETAILER_ADMIN", "RETAILER_STAFF"]))):
    return await return_service.create_return_act(db, data.order_id, data, current_user)

@router.get("/order/{order_id}", response_model=list[ReturnActResponse])
async def get_return_acts(order_id: UUID, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    acts = await db.scalars(select(ReturnAct).where(ReturnAct.order_id == order_id))
    return list(acts.all())

@router.post("/{return_act_id}/accept", response_model=ReturnActResponse)
async def accept_return_act(return_act_id: UUID, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(RoleChecker(["WHOLESALER_ADMIN", "WHOLESALER_MANAGER"]))):
    return await return_service.accept_return_act(db, return_act_id, current_user)

@router.post("/{return_act_id}/dispute", response_model=ReturnActResponse)
async def dispute_return_act(return_act_id: UUID, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(RoleChecker(["WHOLESALER_ADMIN", "WHOLESALER_MANAGER"]))):
    act = await db.scalar(select(ReturnAct).where(ReturnAct.id == return_act_id))
    act.status = ReturnActStatus.DISPUTED
    await db.commit()
    await db.refresh(act)
    return act
