from __future__ import annotations
from typing import Optional
from sqlalchemy import Text, String, Numeric, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from decimal import Decimal
import uuid
from app.models.base import Base, UUIDMixin, TimestampMixin
from app.schemas.common import ReturnActStatus

class ReturnAct(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "return_acts"

    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orders.id"))
    reason: Mapped[str] = mapped_column(Text)
    photo_proof_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[ReturnActStatus] = mapped_column(SQLEnum(ReturnActStatus))
    items: Mapped[list[dict]] = mapped_column(JSONB)
    return_total: Mapped[Decimal] = mapped_column(Numeric(14, 2))

    order: Mapped["Order"] = relationship("Order", back_populates="return_acts")
