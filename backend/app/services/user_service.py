from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.security import hash_password

async def create_user(db: AsyncSession, data: UserCreate) -> User:
    if await db.scalar(select(User).where(User.phone == data.phone)):
        raise HTTPException(status_code=400, detail="Phone already registered")
        
    user_data = data.model_dump()
    user_data["password_hash"] = hash_password(user_data.pop("password"))
    user = User(**user_data)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user(db: AsyncSession, user_id: UUID) -> Optional[User]:
    return await db.scalar(select(User).where(User.id == user_id))

async def list_users(db: AsyncSession, org_id: UUID, page: int, per_page: int):
    query = select(User).where(User.organization_id == org_id)
    result = await db.execute(query.offset((page - 1) * per_page).limit(per_page))
    items = result.scalars().all()
    return {"items": list(items), "total": len(items), "page": page, "per_page": per_page}

async def update_user(db: AsyncSession, user_id: UUID, data: UserUpdate) -> User:
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(user, k, v)
    await db.commit()
    await db.refresh(user)
    return user

async def deactivate_user(db: AsyncSession, user_id: UUID) -> User:
    user = await get_user(db, user_id)
    if user:
        user.is_active = False
        await db.commit()
        await db.refresh(user)
    return user
