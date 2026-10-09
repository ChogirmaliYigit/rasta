from __future__ import annotations
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from app.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import RoleChecker
from app.schemas.common import OrganizationType, OrganizationStatus, UserRole, MessageResponse
from app.schemas.organization import OrganizationCreate, OrganizationUpdate
from app.schemas.user import UserCreate
from app.services import organization_service, user_service

router = APIRouter(prefix="/onboarding", tags=["onboarding"])
superadmin_checker = RoleChecker(["SUPERADMIN"])

class OnboardingApply(BaseModel):
    name: str
    type: OrganizationType
    phone: str
    legal_details: Optional[dict] = None

@router.post("/apply", response_model=MessageResponse)
async def apply(data: OnboardingApply, db: AsyncSession = Depends(get_db)):
    org_data = OrganizationCreate(name=data.name, type=data.type, legal_details=data.legal_details)
    org = await organization_service.create_organization(db, org_data)
    
    role = UserRole.WHOLESALER_ADMIN if data.type == OrganizationType.WHOLESALER else UserRole.RETAILER_ADMIN
    user_data = UserCreate(
        organization_id=org.id,
        full_name=data.name + " Admin",
        phone=data.phone,
        password="temp-password-123",
        role=role
    )
    await user_service.create_user(db, user_data)
    return MessageResponse(message="Application submitted successfully. Waiting for approval.")

@router.get("/applications")
async def list_applications(db: AsyncSession = Depends(get_db), _=Depends(superadmin_checker)):
    return await organization_service.list_organizations(db, 1, 50, status_filter=OrganizationStatus.PENDING)

@router.post("/applications/{org_id}/approve", response_model=MessageResponse)
async def approve_application(org_id: UUID, db: AsyncSession = Depends(get_db), _=Depends(superadmin_checker)):
    await organization_service.update_organization(db, org_id, OrganizationUpdate(status=OrganizationStatus.ACTIVE))
    return MessageResponse(message="Application approved")

@router.post("/applications/{org_id}/reject", response_model=MessageResponse)
async def reject_application(org_id: UUID, db: AsyncSession = Depends(get_db), _=Depends(superadmin_checker)):
    await organization_service.update_organization(db, org_id, OrganizationUpdate(status=OrganizationStatus.SUSPENDED))
    return MessageResponse(message="Application rejected")
