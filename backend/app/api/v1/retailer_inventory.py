from __future__ import annotations
from fastapi import APIRouter, Depends
from uuid import UUID
from app.dependencies import get_db
from app.dependencies import get_current_user, CurrentUser
from app.schemas.inventory import RetailerInventoryResponse
from app.schemas.pos_sale import POSSaleCreate, POSSaleBatchCreate, POSSaleResponse
from app.schemas.common import PaginatedResponse, MessageResponse
from app.services import inventory_service
from sqlalchemy import select
from app.models.inventory import RetailerInventory

router = APIRouter(prefix="/retailer-inventory", tags=["retailer_inventory"])

@router.get("/", response_model=PaginatedResponse[RetailerInventoryResponse])
async def list_inventory(page: int = 1, per_page: int = 50, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    query = select(RetailerInventory).where(RetailerInventory.branch_id == current_user.branch_id)
    result = await db.execute(query.offset((page - 1) * per_page).limit(per_page))
    items = result.scalars().all()
    return {"items": list(items), "total": len(items), "page": page, "per_page": per_page}

@router.post("/pos-sale", response_model=POSSaleResponse)
async def pos_sale(data: POSSaleCreate, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    return await inventory_service.record_pos_sale(db, current_user.branch_id, data)

@router.post("/pos-sale/batch", response_model=list[POSSaleResponse])
async def pos_sale_batch(data: POSSaleBatchCreate, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    return await inventory_service.batch_record_pos_sales(db, current_user.branch_id, data)

@router.get("/low-stock", response_model=list[RetailerInventoryResponse])
async def low_stock(db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    query = select(RetailerInventory).where(RetailerInventory.branch_id == current_user.branch_id, RetailerInventory.current_stock <= RetailerInventory.safety_stock_threshold)
    result = await db.execute(query)
    return list(result.scalars().all())

@router.put("/{inventory_id}/threshold", response_model=MessageResponse)
async def update_threshold(inventory_id: UUID, threshold: int, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    inv = await db.scalar(select(RetailerInventory).where(RetailerInventory.id == inventory_id))
    inv.safety_stock_threshold = threshold
    await db.commit()
    return MessageResponse(message="Threshold updated")
