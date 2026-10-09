import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from app.config import get_settings
from app.models.organization import Organization, Branch
from app.models.user import User
from app.schemas.common import OrganizationType, OrganizationStatus, UserRole
import uuid

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed():
    engine = create_async_engine(settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"))
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Create Superadmin Org
        platform_org = Organization(
            name="Rasta Platform",
            type=OrganizationType.WHOLESALER,
            status=OrganizationStatus.ACTIVE,
            legal_details={"description": "Platform Owner"}
        )
        session.add(platform_org)
        await session.flush()
        
        platform_branch = Branch(
            organization_id=platform_org.id,
            name="HQ"
        )
        session.add(platform_branch)
        await session.flush()
        
        admin_user = User(
            organization_id=platform_org.id,
            branch_id=platform_branch.id,
            phone="+998901234567",
            password_hash=pwd_context.hash("password123"),
            full_name="Super Admin",
            role=UserRole.SUPERADMIN,
            is_active=True
        )
        session.add(admin_user)
        
        # Create Wholesaler Org
        wholesaler_org = Organization(
            name="Global Distribution LLC",
            type=OrganizationType.WHOLESALER,
            status=OrganizationStatus.ACTIVE,
            legal_details={"inn": "123456789"}
        )
        session.add(wholesaler_org)
        await session.flush()
        
        wholesaler_branch = Branch(
            organization_id=wholesaler_org.id,
            name="Main Warehouse"
        )
        session.add(wholesaler_branch)
        await session.flush()
        
        wholesaler_user = User(
            organization_id=wholesaler_org.id,
            branch_id=wholesaler_branch.id,
            phone="+998901111111",
            password_hash=pwd_context.hash("wholesaler123"),
            full_name="Optomchi Ali",
            role=UserRole.WHOLESALER_ADMIN,
            is_active=True
        )
        session.add(wholesaler_user)
        
        await session.commit()
        print("Database seeded successfully!")
        
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(seed())
