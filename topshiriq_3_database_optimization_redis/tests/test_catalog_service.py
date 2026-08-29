import pytest
import json
from database import init_db
from catalog_service import CatalogService
from redis_client import get_redis_client


@pytest.mark.asyncio
async def test_cache_aside_flow():
    await init_db()
    redis = await get_redis_client()
    await redis.flushdb()

    product_id = 1
    cache_key = f"product:{product_id}"

    # 1. Boshida kesh bo'sh bo'lishi kerak
    cached_val = await redis.get(cache_key)
    assert cached_val is None

    # 2. 1-murojaat (Cache Miss -> DB dan oladi va keshga yozadi)
    product_data = await CatalogService.get_product_detail(product_id)
    assert product_data is not None
    assert product_data["id"] == product_id

    # 3. Endi Redis keshida mavjud bo'lishi kerak
    cached_val = await redis.get(cache_key)
    assert cached_val is not None
    cached_dict = json.loads(cached_val)
    assert cached_dict["name"] == product_data["name"]

    # 4. 2-murojaat (Cache Hit -> Redis'dan oladi)
    hit_data = await CatalogService.get_product_detail(product_id)
    assert hit_data == product_data


@pytest.mark.asyncio
async def test_cache_invalidation_on_update():
    await init_db()
    redis = await get_redis_client()
    product_id = 2
    cache_key = f"product:{product_id}"

    # Avval keshga tushiramiz
    p_initial = await CatalogService.get_product_detail(product_id)
    assert p_initial is not None
    assert await redis.get(cache_key) is not None

    # Narxni yangilaymiz -> Kesh o'chishi kerak
    new_price = 1199.0
    updated_product = await CatalogService.update_product_price(product_id, new_price)
    assert updated_product["price"] == new_price

    # Kesh o'chirilganini tekshiramiz
    assert await redis.get(cache_key) is None

    # Yangi so'rov yuborganda yangi narx bilan qaytishi kerak
    refetched = await CatalogService.get_product_detail(product_id)
    assert refetched["price"] == new_price
    assert await redis.get(cache_key) is not None


@pytest.mark.asyncio
async def test_joinedload_optimization():
    await init_db()
    products = await CatalogService.get_products_with_category_optimized()
    assert len(products) > 0
    first = products[0]
    assert "category" in first
    assert first["category"]["id"] is not None
    assert first["category"]["name"] is not None
