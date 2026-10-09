from __future__ import annotations
from typing import Optional
from sqlalchemy import Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from decimal import Decimal
import uuid
from app.models.base import Base, UUIDMixin

class POSSaleLedger(Base, UUIDMixin):
    __tablename__ = "pos_sale_ledger"

    retailer_branch_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("branches.id"))
    global_product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("global_products.id"))
    qty_sold: Mapped[int] = mapped_column(Integer)
    sale_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    sold_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    branch: Mapped["Branch"] = relationship("Branch")
    product: Mapped["GlobalProduct"] = relationship("GlobalProduct")
