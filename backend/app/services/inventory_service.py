from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.models.inventory import RetailerInventory
from app.models.pos_sale import POSSaleLedger
from app.schemas.pos_sale import POSSaleCreate, POSSaleBatchCreate
from app.tasks.notifications import send_reorder_alert

async def record_pos_sale(db: AsyncSession, branch_id: UUID, data: POSSaleCreate) -> POSSaleLedger:
    inv = await db.scalar(select(RetailerInventory).where(RetailerInventory.branch_id == branch_id, RetailerInventory.global_product_id == data.global_product_id))
    if not inv:
        inv = RetailerInventory(branch_id=branch_id, global_product_id=data.global_product_id, current_stock=0)
        db.add(inv)
        
    inv.current_stock -= data.qty_sold
    sale = POSSaleLedger(retailer_branch_id=branch_id, global_product_id=data.global_product_id, qty_sold=data.qty_sold, sale_price=data.sale_price)
    db.add(sale)
    await db.commit()
    await db.refresh(sale)
    
    if inv.current_stock <= inv.safety_stock_threshold and inv.auto_reorder_enabled:
        send_reorder_alert.delay(str(branch_id), str(data.global_product_id), inv.current_stock, inv.safety_stock_threshold)
        
    return sale

async def batch_record_pos_sales(db: AsyncSession, branch_id: UUID, data: POSSaleBatchCreate) -> list[POSSaleLedger]:
    sales = []
    for item in data.items:
        inv = await db.scalar(select(RetailerInventory).where(RetailerInventory.branch_id == branch_id, RetailerInventory.global_product_id == item.global_product_id))
        if not inv:
            inv = RetailerInventory(branch_id=branch_id, global_product_id=item.global_product_id, current_stock=0)
            db.add(inv)
        inv.current_stock -= item.qty_sold
        sale = POSSaleLedger(retailer_branch_id=branch_id, global_product_id=item.global_product_id, qty_sold=item.qty_sold, sale_price=item.sale_price)
        db.add(sale)
        sales.append(sale)
        if inv.current_stock <= inv.safety_stock_threshold and inv.auto_reorder_enabled:
            send_reorder_alert.delay(str(branch_id), str(item.global_product_id), inv.current_stock, inv.safety_stock_threshold)
            
    await db.commit()
    for sale in sales:
        await db.refresh(sale)
    return sales
