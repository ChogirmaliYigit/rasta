from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from fastapi import HTTPException
from app.models.product import GlobalProduct
from app.schemas.product import ProductCreate, ProductUpdate

async def create_product(db: AsyncSession, data: ProductCreate) -> GlobalProduct:
    prod = GlobalProduct(**data.model_dump())
    db.add(prod)
    await db.commit()
    await db.refresh(prod)
    return prod

async def get_product(db: AsyncSession, product_id: UUID) -> Optional[GlobalProduct]:
    return await db.scalar(select(GlobalProduct).where(GlobalProduct.id == product_id))

async def list_products(db: AsyncSession, page: int, per_page: int, category: str = None, search: str = None):
    query = select(GlobalProduct)
    if category:
        query = query.where(GlobalProduct.category == category)
    if search:
        query = query.where(GlobalProduct.title.ilike(f"%{search}%"))
    
    result = await db.execute(query.offset((page - 1) * per_page).limit(per_page))
    items = result.scalars().all()
    return {"items": list(items), "total": len(items), "page": page, "per_page": per_page}

async def update_product(db: AsyncSession, product_id: UUID, data: ProductUpdate) -> GlobalProduct:
    prod = await get_product(db, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(prod, k, v)
    await db.commit()
    await db.refresh(prod)
    return prod

async def search_by_barcode(db: AsyncSession, barcode: str) -> Optional[GlobalProduct]:
    return await db.scalar(select(GlobalProduct).where(GlobalProduct.barcode == barcode))
