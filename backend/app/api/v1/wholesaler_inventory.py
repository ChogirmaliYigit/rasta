from __future__ import annotations
from fastapi import APIRouter, Depends
from typing import Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.dependencies import get_db
from app.dependencies import get_current_user, CurrentUser, RoleChecker
from app.schemas.inventory import WholesalerInventoryCreate, WholesalerInventoryUpdate, WholesalerInventoryResponse, CatalogItemResponse
from app.schemas.common import PaginatedResponse
from app.models.inventory import WholesalerInventory
from app.models.product import GlobalProduct

router = APIRouter(prefix="/wholesaler-inventory", tags=["wholesaler_inventory"])
wholesaler_checker = RoleChecker(["WHOLESALER_ADMIN", "WHOLESALER_MANAGER"])

@router.post("/", response_model=WholesalerInventoryResponse)
async def create_inventory(data: WholesalerInventoryCreate, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(wholesaler_checker)):
    inv = WholesalerInventory(**data.model_dump())
    db.add(inv)
    await db.commit()
    await db.refresh(inv)
    return inv

@router.get("/", response_model=PaginatedResponse[WholesalerInventoryResponse])
async def list_inventory(page: int = 1, per_page: int = 50, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(wholesaler_checker)):
    query = select(WholesalerInventory).where(WholesalerInventory.branch_id == current_user.branch_id)
    result = await db.execute(query.offset((page - 1) * per_page).limit(per_page))
    items = result.scalars().all()
    return {"items": list(items), "total": len(items), "page": page, "per_page": per_page}

@router.put("/{inventory_id}", response_model=WholesalerInventoryResponse)
async def update_inventory(inventory_id: UUID, data: WholesalerInventoryUpdate, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(wholesaler_checker)):
    inv = await db.scalar(select(WholesalerInventory).where(WholesalerInventory.id == inventory_id))
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(inv, k, v)
    await db.commit()
    await db.refresh(inv)
    return inv

@router.patch("/{inventory_id}/stock", response_model=WholesalerInventoryResponse)
async def update_stock(inventory_id: UUID, stock: int, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(wholesaler_checker)):
    inv = await db.scalar(select(WholesalerInventory).where(WholesalerInventory.id == inventory_id))
    inv.available_stock = stock
    await db.commit()
    await db.refresh(inv)
    return inv

@router.get("/catalog", response_model=PaginatedResponse[CatalogItemResponse])
async def catalog(page: int = 1, per_page: int = 50, category: Optional[str] = None, search: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    query = select(WholesalerInventory).options(joinedload(WholesalerInventory.product)).join(GlobalProduct)
    if category:
        query = query.where(GlobalProduct.category == category)
    if search:
        query = query.where(GlobalProduct.title.ilike(f"%{search}%"))
        
    result = await db.execute(query.offset((page - 1) * per_page).limit(per_page))
    items = result.scalars().all()
    
    cat_items = [
        CatalogItemResponse(product=item.product, price=item.price, available_stock=item.available_stock, moq=item.moq)
        for item in items
    ]
    return {"items": cat_items, "total": len(cat_items), "page": page, "per_page": per_page}
