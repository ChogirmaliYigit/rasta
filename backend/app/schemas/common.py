from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import Generic, TypeVar

T = TypeVar("T")

class OrganizationType(str, Enum):
    RETAILER = "RETAILER"
    WHOLESALER = "WHOLESALER"

class OrganizationStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"

class UserRole(str, Enum):
    SUPERADMIN = "SUPERADMIN"
    WHOLESALER_ADMIN = "WHOLESALER_ADMIN"
    WHOLESALER_MANAGER = "WHOLESALER_MANAGER"
    RETAILER_ADMIN = "RETAILER_ADMIN"
    RETAILER_STAFF = "RETAILER_STAFF"
    DRIVER = "DRIVER"

class UnitType(str, Enum):
    PIECE = "PIECE"
    KG = "KG"
    LITRE = "LITRE"
    BOX = "BOX"
    PACK = "PACK"

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    DISPATCHED = "DISPATCHED"
    DELIVERED = "DELIVERED"
    PARTIALLY_RETURNED = "PARTIALLY_RETURNED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class DeliveryType(str, Enum):
    SELF_PICKUP = "SELF_PICKUP"
    WHOLESALER_DELIVERY = "WHOLESALER_DELIVERY"

class ReturnActStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    ACCEPTED = "ACCEPTED"
    DISPUTED = "DISPUTED"

class TransactionType(str, Enum):
    DEBIT_FEE = "DEBIT_FEE"
    CREDIT_PAYMENT = "CREDIT_PAYMENT"
    ADJUSTMENT = "ADJUSTMENT"

class PaginationParams(BaseModel):
    page: int = 1
    per_page: int = 50

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    per_page: int
    
class MessageResponse(BaseModel):
    message: str
