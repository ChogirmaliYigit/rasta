from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from uuid import UUID
from app.models.return_act import ReturnAct
from app.models.order import Order
from app.models.inventory import WholesalerInventory, RetailerInventory
from app.schemas.return_act import ReturnActCreate
from app.schemas.common import ReturnActStatus, OrderStatus
from app.tasks.notifications import notify_return_act

async def create_return_act(db: AsyncSession, order_id: UUID, data: ReturnActCreate, current_user) -> ReturnAct:
    from sqlalchemy.orm import selectinload
    order = await db.scalar(select(Order).options(selectinload(Order.items)).where(Order.id == order_id))
    
    if not order or order.status != OrderStatus.DELIVERED:
        raise HTTPException(status_code=400, detail="Order not eligible for return")
        
    if order.retailer_branch_id != current_user.branch_id:
        raise HTTPException(status_code=403, detail="Forbidden")
        
    return_total = 0
    items_json = []
    
    for r_item in data.items:
        o_item = next((i for i in order.items if i.id == r_item.order_item_id), None)
        if not o_item: raise HTTPException(status_code=400, detail="Invalid item ID")
        if r_item.returned_qty > o_item.delivered_qty: raise HTTPException(status_code=400, detail="Returned qty > delivered qty")
            
        return_total += (r_item.returned_qty * o_item.unit_price)
        items_json.append({"order_item_id": str(r_item.order_item_id), "returned_qty": r_item.returned_qty, "reason": r_item.reason})
        
    act = ReturnAct(
        order_id=order_id, reason=data.reason, photo_proof_url=data.photo_proof_url,
        status=ReturnActStatus.SUBMITTED, items=items_json, return_total=return_total
    )
    
    order.status = OrderStatus.PARTIALLY_RETURNED
    db.add(act)
    await db.commit()
    await db.refresh(act)
    notify_return_act.delay(str(act.id))
    return act

async def accept_return_act(db: AsyncSession, return_act_id: UUID, current_user) -> ReturnAct:
    act = await db.scalar(select(ReturnAct).where(ReturnAct.id == return_act_id))
    if not act or act.status != ReturnActStatus.SUBMITTED:
        raise HTTPException(status_code=400, detail="Invalid return act")
        
    from sqlalchemy.orm import selectinload
    order = await db.scalar(select(Order).options(selectinload(Order.items)).where(Order.id == act.order_id))
    if order.wholesaler_branch_id != current_user.branch_id:
        raise HTTPException(status_code=403, detail="Forbidden")
        
    for r_item in act.items:
        o_item = next((i for i in order.items if str(i.id) == r_item["order_item_id"]), None)
        if o_item:
            o_item.returned_qty += r_item["returned_qty"]
            w_inv = await db.scalar(select(WholesalerInventory).where(WholesalerInventory.branch_id == order.wholesaler_branch_id, WholesalerInventory.global_product_id == o_item.global_product_id))
            if w_inv: w_inv.available_stock += r_item["returned_qty"]
            
            r_inv = await db.scalar(select(RetailerInventory).where(RetailerInventory.branch_id == order.retailer_branch_id, RetailerInventory.global_product_id == o_item.global_product_id))
            if r_inv: r_inv.current_stock -= r_item["returned_qty"]
            
    order.final_amount -= act.return_total
    order.platform_fee = order.final_amount * 0.01
    act.status = ReturnActStatus.ACCEPTED
    await db.commit()
    await db.refresh(act)
    return act
