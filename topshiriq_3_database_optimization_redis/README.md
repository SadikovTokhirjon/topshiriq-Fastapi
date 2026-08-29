# 3-Topshiriq: Database Optimizatsiya va Redis Cache-Aside Servisi

Ushbu loyiha ma'lumotlar bazasini optimallashtirish (SQL Index, EXPLAIN ANALYZE, N+1 muammosi yechimi) hamda Redis Cache-Aside Pattern mexanizmini to'liq qamrab oladi.

---

## 📁 Loyiha Strukturasi

```
topshiriq_3_database_optimization_redis/
├── models.py                 # Category va Product SQLAlchemy modellari (SQL Index)
├── database.py               # Asinxron DB Engine va avtomatik dastlabki ma'lumotlar (seed)
├── redis_client.py           # Redis async client (Haqiqiy Redis va InMemory fallback bilan)
├── catalog_service.py        # CatalogService (Cache-Aside, TTL 300s, Invalidation, joinedload)
├── explain_analysis.py       # SQL so'rovlarini EXPLAIN QUERY PLAN orqali tahlil qiluvchi skript
├── demo.py                   # Barcha bosqichlarni ko'rsatib beruvchi interaktiv namoyish
├── main.py                   # FastAPI REST API (Katalog endpointlari)
├── tests/
│   └── test_catalog_service.py # Pytest asinxron testlari
├── requirements.txt
└── README.md
```

---

## ⚡ Asosiy Konsepsiyalar va Imkoniyatlar

### 1. Redis Cache-Aside Pattern
1. Foydalanuvchi mahsulotni so'raganda, servis avval **Redis keshdan** qidiradi (`product:{product_id}`).
2. **Cache Hit**: Agar keshda mavjud bo'lsa, ma'lumotlar bazasiga murojaat qilmasdan darhol qaytariladi (mikrosoniyalarda).
3. **Cache Miss**: Agar keshda bo'lmasa, ma'lumotlar bazasidan olinadi va Redis'ga **TTL (300 soniya)** bilan saqlanadi.

### 2. Cache Invalidation (Keshni tozalash)
- Mahsulot narxi yoki ma'lumotlari yangilanganda (`update_product_price`), tegishli Redis kaliti (`product:{product_id}`) darhol o'chiriladi (`redis.delete()`).
- Keyingi so'rov to'g'ri va yangilangan ma'lumotni bazadan olib keshlaydi.

### 3. N+1 Muammosining Yechimi (`joinedload`)
- N+1 muammosida 1 ta mahsulotlar so'rovi va N ta kategoriyalar so'rovi (jami 1 + N ta) yuboriladi.
- `CatalogService.get_products_with_category_optimized()` da `joinedload(Product.category)` ishlatilib, barcha ma'lumotlar **bitta SQL JOIN** so'rovida olinadi.

### 4. SQL Index va EXPLAIN ANALYZE
- `Product.name` va `Product.category_id` ustunlariga indeks qo'yilgan bo'lib, ular `Index Scan` orqali millionlab qatorlar ichidan bir zumda topish imkonini beradi.

---

## 🚀 Ishga tushirish

### 1. Interaktiv Namoyishni (Demo) ishga tushirish
Barcha kesh va optimizatsiya bosqichlarini terminalda ko'rish:
```bash
python demo.py
```

### 2. SQL So'rovlarini Tahlil qilish (EXPLAIN ANALYZE)
```bash
python explain_analysis.py
```

### 3. FastAPI REST API ilovasini ishga tushirish
```bash
python main.py
```
yoki:
```bash
uvicorn main:app --reload --port 8001
```
Swagger UI: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

---

## 🧪 Testlarni ishga tushirish

```bash
pytest tests/
```
