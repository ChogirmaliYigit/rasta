from __future__ import annotations
from typing import Optional
from sqlalchemy import String, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base, UUIDMixin, TimestampMixin
from app.schemas.common import OrganizationType, OrganizationStatus
from geoalchemy2 import Geometry
import uuid

class Organization(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[OrganizationType] = mapped_column(SQLEnum(OrganizationType))
    legal_details: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    inn: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)
    status: Mapped[OrganizationStatus] = mapped_column(SQLEnum(OrganizationStatus), default=OrganizationStatus.PENDING)

    branches: Mapped[list["Branch"]] = relationship("Branch", back_populates="organization")
    users: Mapped[list["User"]] = relationship("User", back_populates="organization")
    billing_entries: Mapped[list["BillingLedger"]] = relationship("BillingLedger", back_populates="organization")

class Branch(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "branches"

    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    name: Mapped[str] = mapped_column(String)
    address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    location = mapped_column(Geometry("POINT"), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="branches")
    users: Mapped[list["User"]] = relationship("User", back_populates="branch")
    wholesaler_inventory: Mapped[list["WholesalerInventory"]] = relationship("WholesalerInventory", back_populates="branch")
    retailer_inventory: Mapped[list["RetailerInventory"]] = relationship("RetailerInventory", back_populates="branch")
