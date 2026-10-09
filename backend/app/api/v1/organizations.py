from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from uuid import UUID
from app.dependencies import get_db
from app.dependencies import get_current_user, CurrentUser, RoleChecker
from app.schemas.organization import OrganizationCreate, OrganizationUpdate, OrganizationResponse, BranchCreate, BranchResponse
from app.schemas.common import PaginatedResponse
from app.services import organization_service

router = APIRouter(prefix="/organizations", tags=["organizations"])
superadmin_checker = RoleChecker(["SUPERADMIN"])

@router.post("/", response_model=OrganizationResponse)
async def create_org(data: OrganizationCreate, db: AsyncSession = Depends(get_db), _=Depends(superadmin_checker)):
    return await organization_service.create_organization(db, data)

@router.get("/", response_model=PaginatedResponse[OrganizationResponse])
async def list_orgs(page: int = 1, per_page: int = 50, status_filter: Optional[str] = None, type_filter: Optional[str] = None, db: AsyncSession = Depends(get_db), _=Depends(superadmin_checker)):
    return await organization_service.list_organizations(db, page, per_page, status_filter, type_filter)

@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_org(org_id: UUID, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    if current_user.role != "SUPERADMIN" and current_user.organization_id != org_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    org = await organization_service.get_organization(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Not found")
    return org

@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_org(org_id: UUID, data: OrganizationUpdate, db: AsyncSession = Depends(get_db), _=Depends(superadmin_checker)):
    return await organization_service.update_organization(db, org_id, data)

@router.post("/{org_id}/branches", response_model=BranchResponse)
async def create_branch(org_id: UUID, data: BranchCreate, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    if current_user.role != "SUPERADMIN" and current_user.organization_id != org_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await organization_service.create_branch(db, org_id, data)

@router.get("/{org_id}/branches", response_model=list[BranchResponse])
async def list_branches(org_id: UUID, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    if current_user.role != "SUPERADMIN" and current_user.organization_id != org_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await organization_service.list_branches(db, org_id)
