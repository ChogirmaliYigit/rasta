from __future__ import annotations
from pydantic import BaseModel, ConfigDict, UUID4
from typing import Optional
from datetime import datetime
from app.schemas.common import UserRole

class UserCreate(BaseModel):
    organization_id: UUID4
    branch_id: Optional[UUID4] = None
    full_name: str
    phone: str
    password: str
    role: UserRole
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    branch_id: Optional[UUID4] = None
    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id: UUID4
    organization_id: UUID4
    branch_id: Optional[UUID4]
    full_name: str
    phone: str
    role: UserRole
    is_active: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    model_config = ConfigDict(from_attributes=True)
