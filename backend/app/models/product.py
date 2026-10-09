from __future__ import annotations
from typing import Optional
from sqlalchemy import String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, UUIDMixin, TimestampMixin
from app.schemas.common import UnitType

class GlobalProduct(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "global_products"

    title: Mapped[str] = mapped_column(String, nullable=False)
    barcode: Mapped[Optional[str]] = mapped_column(String, unique=True, index=True, nullable=True)
    sku: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    subcategory: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    unit_type: Mapped[UnitType] = mapped_column(SQLEnum(UnitType))
    image_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
