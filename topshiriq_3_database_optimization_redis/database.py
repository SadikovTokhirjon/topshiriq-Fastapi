import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select, func
from models import Base, Category, Product

DB_URL = os.environ.get("CATALOG_DB_URL", "sqlite+aiosqlite:///./test.db")

engine = create_async_engine(DB_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Jadvallarni yaratish va boshlang'ich ma'lumotlar bilan to'ldirish."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await seed_data()


async def seed_data():
    """Test va namoyish uchun boshlang'ich ma'lumotlar."""
    async with AsyncSessionLocal() as session:
        count_res = await session.execute(select(func.count(Category.id)))
        count = count_res.scalar()

        if count == 0:
            # Kategoriyalar yaratamiz
            electronics = Category(name="Electronics")
            books = Category(name="Books")
            clothing = Category(name="Clothing")

            session.add_all([electronics, books, clothing])
            await session.commit()
            await session.refresh(electronics)
            await session.refresh(books)
            await session.refresh(clothing)

            # Mahsulotlar yaratamiz
            products = [
                Product(name="MacBook Pro 16", price=2499.0, category_id=electronics.id),
                Product(name="iPhone 15 Pro", price=999.0, category_id=electronics.id),
                Product(name="Sony WH-1000XM5", price=349.0, category_id=electronics.id),
                Product(name="Clean Code Book", price=35.0, category_id=books.id),
                Product(name="Designing Data-Intensive Applications", price=45.0, category_id=books.id),
                Product(name="Python Hoodie", price=55.0, category_id=clothing.id),
            ]
            session.add_all(products)
            await session.commit()
