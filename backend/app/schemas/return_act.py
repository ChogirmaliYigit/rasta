from __future__ import annotations
from pydantic import BaseModel, ConfigDict, UUID4
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.schemas.common import ReturnActStatus

class ReturnItemInput(BaseModel):
    order_item_id: UUID4
    returned_qty: int
    reason: str
    model_config = ConfigDict(from_attributes=True)

class ReturnActCreate(BaseModel):
    order_id: UUID4
    reason: str
    items: list[ReturnItemInput]
    photo_proof_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class ReturnActResponse(BaseModel):
    id: UUID4
    order_id: UUID4
    reason: str
    photo_proof_url: Optional[str]
    status: ReturnActStatus
    items: list[dict]
    return_total: Decimal
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
