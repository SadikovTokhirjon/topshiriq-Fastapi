import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from infrastructure.db_models import Base

# Standart SQLite asinxron bazasi (faylda saqlanadi)
DB_PATH = os.environ.get("ORDER_DB_URL", "sqlite+aiosqlite:///./orders.db")

engine = create_async_engine(DB_PATH, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Barcha jadvallarni asinxron tarzda yaratish."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db_session() -> AsyncSession:
    """FastAPI yoki Use case uchun DB session taqdim qilish."""
    async with AsyncSessionLocal() as session:
        yield session
