import asyncio
import time
from database import init_db
from catalog_service import CatalogService
from redis_client import get_redis_client


async def run_full_demo():
    print("=" * 70)
    print("🚀 3-TOPShIRIQ: DATABASE OPTIMIZATSIYA VA REDIS CACHE-ASIDE DEMO")
    print("=" * 70)

    # 1. Bazani sozlash
    print("\n📦 1. Ma'lumotlar bazasi va test yozuvlari tayyorlanmoqda...")
    await init_db()
    redis = await get_redis_client()
    await redis.flushdb()  # Keshni tozalab boshlaymiz
    print("✅ Ma'lumotlar bazasi va Redis tayyor!")

    product_id = 1

    # 2. 1-murojaat (Cache Miss)
    print("\n" + "-" * 50)
    print("🔹 BOSQICH 1: Birinchi murojaat (Kesh bo'sh)")
    print("-" * 50)
    t0 = time.perf_counter()
    p1 = await CatalogService.get_product_detail(product_id)
    t1 = time.perf_counter()
    print(f"📦 Olingan ma'lumot: {p1}")
    print(f"⏱️ Sarflangan vaqt: {(t1 - t0) * 1000:.2f} ms")

    # 3. 2-murojaat (Cache Hit)
    print("\n" + "-" * 50)
    print("🔹 BOSQICH 2: Ikkinchi murojaat (Keshda mavjud)")
    print("-" * 50)
    t0 = time.perf_counter()
    p2 = await CatalogService.get_product_detail(product_id)
    t1 = time.perf_counter()
    print(f"📦 Olingan ma'lumot: {p2}")
    print(f"⏱️ Sarflangan vaqt: {(t1 - t0) * 1000:.2f} ms (Bazaga bormadi, Redis'dan olindi!)")

    # 4. Narxni yangilash va Keshni tozalash (Cache Invalidation)
    print("\n" + "-" * 50)
    print("🔹 BOSQICH 3: Narxni yangilash va Kesh Invalidatsiyasi")
    print("-" * 50)
    new_price = 2799.0
    print(f"✏️ Mahsulot #{product_id} narxi ${new_price} ga o'zgartirilmoqda...")
    updated = await CatalogService.update_product_price(product_id, new_price)
    print(f"✅ Bazadagi yangilangan ma'lumot: {updated}")

    # 5. Yangilanishdan keyingi murojaat (Yana Cache Miss bo'lib, yangi narx keshga tushadi)
    print("\n" + "-" * 50)
    print("🔹 BOSQICH 4: Yangilanishdan keyingi birinchi so'rov")
    print("-" * 50)
    p3 = await CatalogService.get_product_detail(product_id)
    print(f"📦 Olingan yangi ma'lumot: {p3}")

    # 6. N+1 Muammosi va joinedload optimizatsiyasini taqqoslash
    print("\n" + "-" * 50)
    print("🔹 BOSQICH 5: N+1 Muammosi va joinedload Optimizatsiyasi")
    print("-" * 50)

    # N+1 holati (Optimizatsiyasiz)
    _, unopt_queries = await CatalogService.get_products_with_category_unoptimized()
    print(f"🐢 Optimizatsiyasiz yondashuv: Jami {unopt_queries} ta SQL so'rovi yuborildi (1 + N muammosi)!")

    # Optimizatsiyalangan holat (joinedload)
    opt_products = await CatalogService.get_products_with_category_optimized()
    print(f"⚡ Optimizatsiyalangan yondashuv (joinedload): Faqat 1 ta SQL JOIN so'rovi bilan {len(opt_products)} ta mahsulot va kategoriyalari yuklandi!")

    print("\n" + "=" * 70)
    print("🎉 Barcha amaliyotlar muvaffaqiyatli yakunlandi!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_full_demo())
