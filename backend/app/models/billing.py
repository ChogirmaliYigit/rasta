from __future__ import annotations
from typing import Optional
from sqlalchemy import Text, Numeric, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from decimal import Decimal
import uuid
from app.models.base import Base, UUIDMixin
from app.schemas.common import TransactionType

class BillingLedger(Base, UUIDMixin):
    __tablename__ = "billing_ledger"

    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    transaction_type: Mapped[TransactionType] = mapped_column(SQLEnum(TransactionType))
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    balance_after: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    reference_order_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("orders.id"), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    organization: Mapped["Organization"] = relationship("Organization", back_populates="billing_entries")
    reference_order: Mapped["Order"] = relationship("Order")
