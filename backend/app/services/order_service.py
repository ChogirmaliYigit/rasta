from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from datetime import datetime, timezone
import uuid
from fastapi import HTTPException
from app.models.order import Order, OrderItem
from app.models.inventory import WholesalerInventory, RetailerInventory
from app.models.organization import Branch
from app.schemas.order import OrderCreate
from app.schemas.common import OrderStatus
from app.tasks.notifications import notify_wholesaler_new_order

async def create_order(db: AsyncSession, retailer_branch_id: UUID, data: OrderCreate) -> Order:
    # 1. Validate branches
    ret_branch = await db.scalar(select(Branch).where(Branch.id == retailer_branch_id))
    if not ret_branch: raise HTTPException(status_code=404, detail="Retailer branch not found")
    
    ws_branch = await db.scalar(select(Branch).where(Branch.id == data.wholesaler_branch_id))
    if not ws_branch: raise HTTPException(status_code=404, detail="Wholesaler branch not found")

    total_amount = 0
    order_items = []
    
    # 3. For each item: SELECT FOR UPDATE
    for item in data.items:
        inv = await db.scalar(
            select(WholesalerInventory)
            .where(WholesalerInventory.branch_id == data.wholesaler_branch_id)
            .where(WholesalerInventory.global_product_id == item.global_product_id)
            .with_for_update()
        )
        if not inv:
            raise HTTPException(status_code=409, detail=f"Product {item.global_product_id} not available")
            
        available_real = inv.available_stock - inv.reserved_stock
        if available_real < item.qty:
            raise HTTPException(status_code=409, detail=f"Insufficient stock for {item.global_product_id}")
            
        if item.qty < inv.moq:
            raise HTTPException(status_code=409, detail=f"MOQ for {item.global_product_id} is {inv.moq}")
            
        inv.reserved_stock += item.qty
        
        line_total = item.qty * inv.price
        total_amount += line_total
        
        order_items.append(OrderItem(
            global_product_id=item.global_product_id,
            ordered_qty=item.qty,
            delivered_qty=item.qty,
            unit_price=inv.price,
            line_total=line_total
        ))
        
    platform_fee = total_amount * 0.01
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    order_number = f"ORD-{date_str}-{str(uuid.uuid4())[:8].upper()}"
    
    order = Order(
        order_number=order_number,
        retailer_branch_id=retailer_branch_id,
        wholesaler_branch_id=data.wholesaler_branch_id,
        status=OrderStatus.PENDING,
        delivery_type=data.delivery_type,
        total_amount=total_amount,
        platform_fee=platform_fee,
        final_amount=total_amount,
        notes=data.notes,
        items=order_items
    )
    
    db.add(order)
    await db.commit()
    await db.refresh(order)
    
    notify_wholesaler_new_order.delay(str(order.id))
    return order

async def update_order_status(db: AsyncSession, order_id: UUID, new_status: OrderStatus, current_user) -> Order:
    from sqlalchemy.orm import selectinload
    stmt = select(Order).options(selectinload(Order.items)).where(Order.id == order_id)
    order = await db.scalar(stmt)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    if order.status == OrderStatus.PENDING and new_status == OrderStatus.CONFIRMED:
        for item in order.items:
            inv = await db.scalar(select(WholesalerInventory).where(WholesalerInventory.branch_id == order.wholesaler_branch_id, WholesalerInventory.global_product_id == item.global_product_id))
            if inv:
                inv.reserved_stock -= item.ordered_qty
                inv.available_stock -= item.ordered_qty
    elif order.status == OrderStatus.PENDING and new_status == OrderStatus.CANCELLED:
        for item in order.items:
            inv = await db.scalar(select(WholesalerInventory).where(WholesalerInventory.branch_id == order.wholesaler_branch_id, WholesalerInventory.global_product_id == item.global_product_id))
            if inv: inv.reserved_stock -= item.ordered_qty
    elif order.status == OrderStatus.DISPATCHED and new_status == OrderStatus.DELIVERED:
        for item in order.items:
            item.delivered_qty = item.ordered_qty
            inv = await db.scalar(select(RetailerInventory).where(RetailerInventory.branch_id == order.retailer_branch_id, RetailerInventory.global_product_id == item.global_product_id))
            if inv:
                inv.current_stock += item.delivered_qty
            else:
                db.add(RetailerInventory(branch_id=order.retailer_branch_id, global_product_id=item.global_product_id, current_stock=item.delivered_qty))
                
    order.status = new_status
    await db.commit()
    await db.refresh(order)
    return order

async def get_order(db: AsyncSession, order_id: UUID) -> Optional[Order]:
    from sqlalchemy.orm import selectinload
    return await db.scalar(select(Order).options(selectinload(Order.items)).where(Order.id == order_id))

async def list_orders(db: AsyncSession, branch_id: UUID, role: str, page: int, per_page: int, status_filter: str = None):
    query = select(Order)
    if "RETAILER" in role:
        query = query.where(Order.retailer_branch_id == branch_id)
    elif "WHOLESALER" in role:
        query = query.where(Order.wholesaler_branch_id == branch_id)
        
    if status_filter:
        query = query.where(Order.status == status_filter)
        
    result = await db.execute(query.offset((page - 1) * per_page).limit(per_page))
    items = result.scalars().all()
    return {"items": list(items), "total": len(items), "page": page, "per_page": per_page}
