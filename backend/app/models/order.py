from __future__ import annotations
from typing import Optional
from sqlalchemy import String, Text, Numeric, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
import uuid
from app.models.base import Base, UUIDMixin, TimestampMixin
from app.schemas.common import OrderStatus, DeliveryType

class Order(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "orders"

    order_number: Mapped[str] = mapped_column(String, unique=True, index=True)
    retailer_branch_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("branches.id"))
    wholesaler_branch_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("branches.id"))
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus))
    delivery_type: Mapped[DeliveryType] = mapped_column(SQLEnum(DeliveryType))
    total_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    platform_fee: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    final_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    retailer_branch: Mapped["Branch"] = relationship("Branch", foreign_keys=[retailer_branch_id])
    wholesaler_branch: Mapped["Branch"] = relationship("Branch", foreign_keys=[wholesaler_branch_id])
    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")
    return_acts: Mapped[list["ReturnAct"]] = relationship("ReturnAct", back_populates="order")

class OrderItem(Base, UUIDMixin):
    __tablename__ = "order_items"

    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    global_product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("global_products.id"))
    ordered_qty: Mapped[int] = mapped_column(Integer)
    delivered_qty: Mapped[int] = mapped_column(Integer)
    returned_qty: Mapped[int] = mapped_column(Integer, default=0)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    line_total: Mapped[Decimal] = mapped_column(Numeric(14, 2))

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["GlobalProduct"] = relationship("GlobalProduct")
