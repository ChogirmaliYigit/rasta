from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
import uuid
from app.models.user import User
from app.schemas.auth import TokenResponse
from app.security import verify_password, hash_password, create_access_token, create_refresh_token, decode_token

async def authenticate_user(db: AsyncSession, phone: str, password: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.phone == phone))
    user = result.scalar_one_or_none()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def create_user_tokens(user: User) -> TokenResponse:
    jti = str(uuid.uuid4())
    access_token = create_access_token(
        subject=str(user.id),
        org_id=str(user.organization_id),
        role=user.role,
        jti=jti
    )
    refresh_token = create_refresh_token(
        subject=str(user.id),
        org_id=str(user.organization_id),
        role=user.role,
        jti=jti
    )
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

async def refresh_user_tokens(db: AsyncSession, refresh_token: str) -> TokenResponse:
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
        
    return create_user_tokens(user)

async def change_user_password(db: AsyncSession, user_id: uuid.UUID, old_password: str, new_password: str):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user or not verify_password(old_password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect old password")
    
    user.password_hash = hash_password(new_password)
    await db.commit()
