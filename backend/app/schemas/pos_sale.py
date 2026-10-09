from __future__ import annotations
from pydantic import BaseModel, ConfigDict, UUID4
from typing import Optional
from datetime import datetime
from decimal import Decimal

class POSSaleCreate(BaseModel):
    global_product_id: UUID4
    qty_sold: int
    sale_price: Optional[Decimal] = None
    model_config = ConfigDict(from_attributes=True)

class POSSaleBatchCreate(BaseModel):
    items: list[POSSaleCreate]
    model_config = ConfigDict(from_attributes=True)

class POSSaleResponse(BaseModel):
    id: UUID4
    retailer_branch_id: UUID4
    global_product_id: UUID4
    qty_sold: int
    sale_price: Optional[Decimal]
    sold_at: datetime
    model_config = ConfigDict(from_attributes=True)
