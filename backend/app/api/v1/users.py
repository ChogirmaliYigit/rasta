from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from app.dependencies import get_db
from app.dependencies import get_current_user, CurrentUser, RoleChecker
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.common import PaginatedResponse, MessageResponse
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])
admin_checker = RoleChecker(["SUPERADMIN", "WHOLESALER_ADMIN", "RETAILER_ADMIN"])

@router.post("/", response_model=UserResponse)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db), _=Depends(admin_checker)):
    return await user_service.create_user(db, data)

@router.get("/", response_model=PaginatedResponse[UserResponse])
async def list_users(page: int = 1, per_page: int = 50, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    return await user_service.list_users(db, current_user.organization_id, page, per_page)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    user = await user_service.get_user(db, user_id)
    if not user or (current_user.role != "SUPERADMIN" and user.organization_id != current_user.organization_id):
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: UUID, data: UserUpdate, db: AsyncSession = Depends(get_db), _=Depends(admin_checker)):
    return await user_service.update_user(db, user_id, data)

@router.delete("/{user_id}", response_model=MessageResponse)
async def deactivate_user(user_id: UUID, db: AsyncSession = Depends(get_db), _=Depends(admin_checker)):
    await user_service.deactivate_user(db, user_id)
    return MessageResponse(message="User deactivated successfully")
