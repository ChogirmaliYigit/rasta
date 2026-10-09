from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from uuid import UUID
from app.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import RoleChecker
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.schemas.common import PaginatedResponse
from app.services import product_service

router = APIRouter(prefix="/products", tags=["products"])
superadmin_checker = RoleChecker(["SUPERADMIN"])

@router.post("/", response_model=ProductResponse)
async def create_product(data: ProductCreate, db: AsyncSession = Depends(get_db), _=Depends(superadmin_checker)):
    return await product_service.create_product(db, data)

@router.get("/", response_model=PaginatedResponse[ProductResponse])
async def list_products(page: int = 1, per_page: int = 50, category: Optional[str] = None, search: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    return await product_service.list_products(db, page, per_page, category, search)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: UUID, db: AsyncSession = Depends(get_db)):
    prod = await product_service.get_product(db, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: UUID, data: ProductUpdate, db: AsyncSession = Depends(get_db), _=Depends(superadmin_checker)):
    return await product_service.update_product(db, product_id, data)

@router.get("/barcode/{barcode}", response_model=ProductResponse)
async def get_product_by_barcode(barcode: str, db: AsyncSession = Depends(get_db)):
    prod = await product_service.search_by_barcode(db, barcode)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod
