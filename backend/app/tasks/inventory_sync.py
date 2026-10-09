from __future__ import annotations
from app.tasks.celery_app import celery_app
from app.tasks.database import get_sync_db
from app.models.inventory import WholesalerInventory

@celery_app.task
def sync_erp_stock(branch_id: str, stock_data: list[dict]):
    db = next(get_sync_db())
    for item in stock_data:
        inv = db.query(WholesalerInventory).filter(
            WholesalerInventory.branch_id == branch_id,
            WholesalerInventory.global_product_id == item["product_id"]
        ).first()
        if inv:
            inv.available_stock = item["stock"]
    db.commit()
