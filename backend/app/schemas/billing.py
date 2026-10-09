from __future__ import annotations
from pydantic import BaseModel, ConfigDict, UUID4
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.schemas.common import TransactionType

class CreditPaymentCreate(BaseModel):
    amount: Decimal
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class BillingEntryResponse(BaseModel):
    id: UUID4
    organization_id: UUID4
    transaction_type: TransactionType
    amount: Decimal
    balance_after: Decimal
    reference_order_id: Optional[UUID4]
    description: Optional[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class BillingStatementResponse(BaseModel):
    current_balance: Decimal
    entries: list[BillingEntryResponse]
    model_config = ConfigDict(from_attributes=True)
