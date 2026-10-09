from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from uuid import UUID
from app.dependencies import get_db
from app.dependencies import get_current_user, CurrentUser, RoleChecker
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse, OrderDetailResponse
from app.schemas.common import PaginatedResponse
from app.services import order_service

router = APIRouter(prefix="/orders", tags=["orders"])
retailer_checker = RoleChecker(["RETAILER_ADMIN", "RETAILER_STAFF"])

@router.post("/", response_model=OrderResponse)
async def create_order(data: OrderCreate, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(retailer_checker)):
    return await order_service.create_order(db, current_user.branch_id, data)

@router.get("/", response_model=PaginatedResponse[OrderResponse])
async def list_orders(page: int = 1, per_page: int = 50, status_filter: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    return await order_service.list_orders(db, current_user.branch_id, current_user.role, page, per_page, status_filter)

@router.get("/{order_id}", response_model=OrderDetailResponse)
async def get_order(order_id: UUID, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    order = await order_service.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_status(order_id: UUID, data: OrderUpdate, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    return await order_service.update_order_status(db, order_id, data.status, current_user)

@router.post("/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(order_id: UUID, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    from app.schemas.common import OrderStatus
    return await order_service.update_order_status(db, order_id, OrderStatus.CANCELLED, current_user)
