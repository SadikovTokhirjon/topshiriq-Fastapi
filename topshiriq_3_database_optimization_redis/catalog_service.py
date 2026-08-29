import json
from typing import Optional, Dict, Any, List
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from models import Product, Category
from database import AsyncSessionLocal
from redis_client import get_redis_client


class CatalogService:
    """
    3-Loyiha: Database Optimizatsiya va Redis Cache-Aside Servisi.
    - Redis Cache-Aside Pattern
    - TTL (Time To Live) boshqaruvi
    - Cache Invalidation (Ma'lumot yangilanganda keshni o'chirish)
    - N+1 muammosini joinedload orqali bitta SQL so'roviga tushirish
    """

    @staticmethod
    async def get_product_detail(product_id: int) -> Optional[Dict[str, Any]]:
        """
        Cache-Aside Pattern:
        1. Redis keshdan qidirish (Cache Hit)
        2. Topilmasa DB'dan olish (Cache Miss)
        3. DB'dan olingan ma'lumotni TTL (300 soniya) bilan Redis'ga saqlash
        """
        redis = await get_redis_client()
        cache_key = f"product:{product_id}"

        # 1-Qadam: Redis Cache Check (Cache Hit)
        cached_product = await redis.get(cache_key)
        if cached_product:
            print(f"⚡ [CACHE HIT] Mahsulot #{product_id} Redis keshidan qaytarildi!")
            return json.loads(cached_product)

        # 2-Qadam: Database Fetch with Query Optimization (Cache Miss)
        print(f"🐢 [CACHE MISS] Mahsulot #{product_id} Bazadan qidirilmoqda...")
        async with AsyncSessionLocal() as session:
            stmt = select(Product).where(Product.id == product_id)
            result = await session.execute(stmt)
            product = result.scalar_one_or_none()

            if not product:
                return None

            product_dict = {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "category_id": product.category_id,
            }

            # 3-Qadam: Write to Redis with TTL (300 seconds)
            await redis.set(cache_key, json.dumps(product_dict), ex=300)
            return product_dict

    @staticmethod
    async def update_product_price(product_id: int, new_price: float) -> Optional[Dict[str, Any]]:
        """
        Kesh invalidatsiyasi (Cache Invalidation):
        Ma'lumot yangilanganda DB'ga yoziladi va tegishli Redis kaliti darhol o'chiriladi.
        """
        redis = await get_redis_client()
        async with AsyncSessionLocal() as session:
            stmt = select(Product).where(Product.id == product_id)
            res = await session.execute(stmt)
            product = res.scalar_one_or_none()

            if not product:
                return None

            product.price = new_price
            await session.commit()
            await session.refresh(product)

            # Redis Keshni invalidate qilish (o'chirish)
            cache_key = f"product:{product_id}"
            await redis.delete(cache_key)
            print(f"🗑️ {cache_key} keshi muvaffaqiyatli tozalandi (Cache Invalidation)!")

            return {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "category_id": product.category_id,
            }

    @staticmethod
    async def get_products_with_category_optimized() -> List[Dict[str, Any]]:
        """
        N+1 Muammosining Yechimi:
        `joinedload` orqali Category va Product bitta SQL JOIN so'rovi bilan olinadi (1 ta so'rov).
        """
        async with AsyncSessionLocal() as session:
            stmt = select(Product).options(joinedload(Product.category))
            result = await session.execute(stmt)
            products = result.scalars().all()

            output = []
            for p in products:
                output.append({
                    "id": p.id,
                    "name": p.name,
                    "price": p.price,
                    "category": {
                        "id": p.category.id if p.category else None,
                        "name": p.category.name if p.category else None,
                    },
                })
            return output

    @staticmethod
    async def get_products_with_category_unoptimized() -> tuple[List[Dict[str, Any]], int]:
        """
        N+1 Muammosi namoyishi:
        1 ta so'rov barcha mahsulotlar uchun + N ta alohida so'rov har bir mahsulot kategoriyasi uchun.
        Jami so'rovlar soni: 1 + N
        """
        query_count = 0
        async with AsyncSessionLocal() as session:
            # 1-so'rov: Mahsulotlar ro'yxati
            stmt = select(Product)
            result = await session.execute(stmt)
            products = result.scalars().all()
            query_count += 1

            output = []
            for p in products:
                # N ta qo'shimcha so'rov har bir mahsulot kategoriyasi uchun
                cat_stmt = select(Category).where(Category.id == p.category_id)
                cat_res = await session.execute(cat_stmt)
                cat = cat_res.scalar_one_or_none()
                query_count += 1

                output.append({
                    "id": p.id,
                    "name": p.name,
                    "price": p.price,
                    "category": {
                        "id": cat.id if cat else None,
                        "name": cat.name if cat else None,
                    },
                })
            return output, query_count
