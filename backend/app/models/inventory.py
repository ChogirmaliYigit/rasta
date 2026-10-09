from __future__ import annotations
from typing import Optional
from sqlalchemy import ForeignKey, Numeric, Integer, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
import uuid
from app.models.base import Base, UUIDMixin, TimestampMixin

class WholesalerInventory(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "wholesaler_inventory"

    branch_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("branches.id"))
    global_product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("global_products.id"))
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    moq: Mapped[int] = mapped_column(Integer, default=1)
    available_stock: Mapped[int] = mapped_column(Integer, default=0)
    reserved_stock: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    branch: Mapped["Branch"] = relationship("Branch", back_populates="wholesaler_inventory")
    product: Mapped["GlobalProduct"] = relationship("GlobalProduct")

    __table_args__ = (
        UniqueConstraint("branch_id", "global_product_id"),
    )

class RetailerInventory(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "retailer_inventory"

    branch_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("branches.id"))
    global_product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("global_products.id"))
    current_stock: Mapped[int] = mapped_column(Integer, default=0)
    safety_stock_threshold: Mapped[int] = mapped_column(Integer, default=10)
    auto_reorder_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    branch: Mapped["Branch"] = relationship("Branch", back_populates="retailer_inventory")
    product: Mapped["GlobalProduct"] = relationship("GlobalProduct")

    __table_args__ = (
        UniqueConstraint("branch_id", "global_product_id"),
    )
