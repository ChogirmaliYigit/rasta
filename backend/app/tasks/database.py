from __future__ import annotations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.config import get_settings

settings = get_settings()

sync_database_url = settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql")

engine = create_engine(
    sync_database_url,
    poolclass=NullPool,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_sync_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
