from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from fastapi import HTTPException
from app.models.organization import Organization, Branch
from app.schemas.organization import OrganizationCreate, OrganizationUpdate, BranchCreate, BranchUpdate
from app.schemas.common import OrganizationStatus

async def create_organization(db: AsyncSession, data: OrganizationCreate) -> Organization:
    org = Organization(**data.model_dump())
    db.add(org)
    await db.commit()
    await db.refresh(org)
    return org

async def get_organization(db: AsyncSession, org_id: UUID) -> Optional[Organization]:
    return await db.scalar(select(Organization).where(Organization.id == org_id))

async def list_organizations(db: AsyncSession, page: int, per_page: int, status_filter: str = None, type_filter: str = None):
    query = select(Organization)
    if status_filter:
        query = query.where(Organization.status == status_filter)
    if type_filter:
        query = query.where(Organization.type == type_filter)
    
    result = await db.execute(query.offset((page - 1) * per_page).limit(per_page))
    items = result.scalars().all()
    
    return {"items": list(items), "total": len(items), "page": page, "per_page": per_page}

async def update_organization(db: AsyncSession, org_id: UUID, data: OrganizationUpdate) -> Organization:
    org = await get_organization(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(org, k, v)
    await db.commit()
    await db.refresh(org)
    return org

async def create_branch(db: AsyncSession, org_id: UUID, data: BranchCreate) -> Branch:
    branch = Branch(**data.model_dump(), organization_id=org_id)
    db.add(branch)
    await db.commit()
    await db.refresh(branch)
    return branch

async def list_branches(db: AsyncSession, org_id: UUID) -> list[Branch]:
    result = await db.execute(select(Branch).where(Branch.organization_id == org_id))
    return list(result.scalars().all())
