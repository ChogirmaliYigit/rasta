from __future__ import annotations
from pydantic import BaseModel, ConfigDict, UUID4
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.schemas.product import ProductResponse

class WholesalerInventoryCreate(BaseModel):
    branch_id: UUID4
    global_product_id: UUID4
    price: Decimal
    moq: int = 1
    available_stock: int = 0
    model_config = ConfigDict(from_attributes=True)

class WholesalerInventoryUpdate(BaseModel):
    price: Optional[Decimal] = None
    moq: Optional[int] = None
    available_stock: Optional[int] = None
    reserved_stock: Optional[int] = None
    is_active: Optional[bool] = None
    model_config = ConfigDict(from_attributes=True)

class WholesalerInventoryResponse(BaseModel):
    id: UUID4
    branch_id: UUID4
    global_product_id: UUID4
    price: Decimal
    moq: int
    available_stock: int
    reserved_stock: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class RetailerInventoryResponse(BaseModel):
    id: UUID4
    branch_id: UUID4
    global_product_id: UUID4
    current_stock: int
    safety_stock_threshold: int
    auto_reorder_enabled: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CatalogItemResponse(BaseModel):
    product: ProductResponse
    price: Decimal
    available_stock: int
    moq: int
    model_config = ConfigDict(from_attributes=True)
