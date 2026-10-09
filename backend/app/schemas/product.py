from __future__ import annotations
from pydantic import BaseModel, ConfigDict, UUID4
from typing import Optional
from datetime import datetime
from app.schemas.common import UnitType

class ProductCreate(BaseModel):
    title: str
    barcode: Optional[str] = None
    sku: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    unit_type: UnitType
    image_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    barcode: Optional[str] = None
    sku: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    unit_type: Optional[UnitType] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
    model_config = ConfigDict(from_attributes=True)

class ProductResponse(BaseModel):
    id: UUID4
    title: str
    barcode: Optional[str]
    sku: Optional[str]
    category: Optional[str]
    subcategory: Optional[str]
    unit_type: UnitType
    image_url: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
