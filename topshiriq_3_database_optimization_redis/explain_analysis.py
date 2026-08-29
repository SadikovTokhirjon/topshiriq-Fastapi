import asyncio
from sqlalchemy import text
from database import AsyncSessionLocal, init_db


async def run_explain_analysis():
    """
    SQL so'rovlarini EXPLAIN / EXPLAIN QUERY PLAN orqali tahlil qilish.
    - SQL Indeksli ustun bo'yicha qidiruv (Index Scan)
    - Indekssiz qidiruv (Scan / Seq Scan)
    """
    await init_db()

    print("=" * 65)
    print("📊 3-TOPShIRIQ: SQL SO'ROV TAHLILI (EXPLAIN QUERY PLAN)")
    print("=" * 65)

    async with AsyncSessionLocal() as session:
        # 1. Indeksli so'rov tahlili (Product.name da index=True bor)
        indexed_query = text("EXPLAIN QUERY PLAN SELECT * FROM products WHERE name = 'MacBook Pro 16'")
        res_indexed = await session.execute(indexed_query)
        rows_indexed = res_indexed.fetchall()

        print("\n🔍 1. INDEKSLI USTUN BO'YICHA SO'ROV (`name` ustuni):")
        print("   SQL: SELECT * FROM products WHERE name = 'MacBook Pro 16'")
        for row in rows_indexed:
            print(f"   [Reja]: {row}")
        print("   ⚡ Natija: Qidiruv 'SEARCH TABLE products USING INDEX' orqali amalga oshirildi (Juda tez).")

        # 2. Indekssiz so'rov tahlili (`price` ustunida indeks yo'q)
        unindexed_query = text("EXPLAIN QUERY PLAN SELECT * FROM products WHERE price > 500.0")
        res_unindexed = await session.execute(unindexed_query)
        rows_unindexed = res_unindexed.fetchall()

        print("\n🔍 2. INDEKSSIZ USTUN BO'YICHA SO'ROV (`price` ustuni):")
        print("   SQL: SELECT * FROM products WHERE price > 500.0")
        for row in rows_unindexed:
            print(f"   [Reja]: {row}")
        print("   🐢 Natija: Qidiruv 'SCAN TABLE products' (Sequential Scan) orqali barcha qatorlar ko'rib chiqiladi.")

        # 3. JOIN va N+1 optimizatsiyasi tahlili
        join_query = text(
            "EXPLAIN QUERY PLAN SELECT products.*, categories.* FROM products "
            "JOIN categories ON products.category_id = categories.id"
        )
        res_join = await session.execute(join_query)
        rows_join = res_join.fetchall()

        print("\n🔍 3. OPTIMALLASHTIRILGAN JOIN SO'ROVI (N+1 muammosi yechimi):")
        print("   SQL: SELECT ... FROM products JOIN categories ON products.category_id = categories.id")
        for row in rows_join:
            print(f"   [Reja]: {row}")
        print("   ✅ Natija: Barcha mahsulotlar va ularning kategoriyalari 1 ta so'rovda JOIN bilan yuklanadi.")
    print("=" * 65)


if __name__ == "__main__":
    asyncio.run(run_explain_analysis())
