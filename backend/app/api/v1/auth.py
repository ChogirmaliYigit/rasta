from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest, ChangePasswordRequest
from app.schemas.user import UserResponse
from app.schemas.common import MessageResponse
from app.dependencies import get_db
from app.dependencies import get_current_user, CurrentUser
from app.services.auth_service import authenticate_user, create_user_tokens, refresh_user_tokens, change_user_password
from app.models.user import User
from sqlalchemy import select
from datetime import datetime, timezone

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, req.phone, req.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    user.last_login = datetime.now(timezone.utc)
    await db.commit()
    return create_user_tokens(user)

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(req: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    return await refresh_user_tokens(db, req.refresh_token)

@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    req: ChangePasswordRequest, 
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    await change_user_password(db, current_user.id, req.old_password, req.new_password)
    return MessageResponse(message="Password changed successfully")

@router.get("/me", response_model=UserResponse)
async def get_me(db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    result = await db.execute(select(User).where(User.id == current_user.id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
