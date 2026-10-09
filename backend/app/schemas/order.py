from __future__ import annotations
from pydantic import BaseModel, ConfigDict, UUID4
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.schemas.common import OrderStatus, DeliveryType
from app.schemas.product import ProductResponse

class OrderItemCreate(BaseModel):
    global_product_id: UUID4
    qty: int
    model_config = ConfigDict(from_attributes=True)

class OrderCreate(BaseModel):
    wholesaler_branch_id: UUID4
    delivery_type: DeliveryType
    items: list[OrderItemCreate]
    notes: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class OrderUpdate(BaseModel):
    status: OrderStatus
    model_config = ConfigDict(from_attributes=True)

class OrderItemResponse(BaseModel):
    id: UUID4
    order_id: UUID4
    global_product_id: UUID4
    ordered_qty: int
    delivered_qty: int
    returned_qty: int
    unit_price: Decimal
    line_total: Decimal
    product: Optional[ProductResponse] = None
    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    id: UUID4
    order_number: str
    retailer_branch_id: UUID4
    wholesaler_branch_id: UUID4
    status: OrderStatus
    delivery_type: DeliveryType
    total_amount: Decimal
    platform_fee: Decimal
    final_amount: Decimal
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class OrderDetailResponse(OrderResponse):
    items: list[OrderItemResponse]
    model_config = ConfigDict(from_attributes=True)
