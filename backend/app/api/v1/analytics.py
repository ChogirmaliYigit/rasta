from __future__ import annotations
from fastapi import APIRouter, Depends
from app.dependencies import get_db
from app.dependencies import get_current_user, CurrentUser

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/dashboard")
async def get_dashboard(db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    return {
        "total_orders": 100,
        "total_revenue": 50000.0,
        "pending_orders": 5,
        "active_products": 200,
        "orders_by_status": {"PENDING": 5, "CONFIRMED": 50, "DELIVERED": 45},
        "revenue_by_month": [{"month": "2024-01", "revenue": 10000}],
        "top_products": [{"title": "Product A", "volume": 500}]
    }
