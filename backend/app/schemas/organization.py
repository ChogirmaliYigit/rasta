from __future__ import annotations
from pydantic import BaseModel, ConfigDict, UUID4
from typing import Optional
from datetime import datetime
from app.schemas.common import OrganizationType, OrganizationStatus

class OrganizationCreate(BaseModel):
    name: str
    type: OrganizationType
    legal_details: Optional[dict] = None
    inn: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    legal_details: Optional[dict] = None
    inn: Optional[str] = None
    status: Optional[OrganizationStatus] = None
    model_config = ConfigDict(from_attributes=True)

class OrganizationResponse(BaseModel):
    id: UUID4
    name: str
    type: OrganizationType
    legal_details: Optional[dict]
    inn: Optional[str]
    status: OrganizationStatus
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class BranchCreate(BaseModel):
    organization_id: UUID4
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class BranchUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    model_config = ConfigDict(from_attributes=True)

class BranchResponse(BaseModel):
    id: UUID4
    organization_id: UUID4
    name: str
    address: Optional[str]
    phone: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
