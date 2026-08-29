# 1-Topshiriq: Clean Architecture bo'yicha "E-Commerce Buyurtmalarni Boshqarish API"

Ushbu loyiha Clean Architecture (Aniq Arxitektura) tamoyillari asosida ishlab chiqilgan bo'lib, biznes-mantiq (Domain va Use Cases) tashqi kutubxonalar (FastAPI, SQLAlchemy, Database) o'zgarganda ham o'zgarishsiz qolishi ta'minlangan.

---

## 🏗️ Arxitektura Qatlamlari

```
topshiriq_1_clean_architecture/
├── domain/                  # 1. Domain qatlami (Pure Python)
│   ├── models.py            # Biznes entitylar (Order, OrderItem, total_price)
│   └── repository_interface.py # Repository interfeysi (DIP - Dependency Inversion)
├── use_cases/               # 2. Use Cases qatlami (Application Rules)
│   └── create_order.py      # Biznes qoidalar (min 10$, kamida 1 mahsulot)
├── infrastructure/          # 3. Infrastructure qatlami (DB, ORM)
│   ├── database.py          # Asinxron SQLite / PostgreSQL engine
│   ├── db_models.py         # SQLAlchemy deklarativ jadvallari
│   └── sql_repository.py    # Repository interfeysi realizatsiyasi
├── api/                     # 4. Interface Adapters / API qatlami (FastAPI)
│   └── router.py            # REST API Controller va Pydantic sxemalar
├── tests/                   # Avtomatlashtirilgan testlar
│   ├── test_use_cases.py    # DBsiz Use Case unit testlari
│   └── test_api.py          # API integratsiya testlari
├── main.py                  # FastAPI ilovasini ishga tushiruvchi kirish nuqtasi
└── requirements.txt
```

---

## ⚡ Asosiy Imkoniyatlar

1. **Pure Domain Entities**: Biznes qoidalar hech qanday tashqi frameworkka bog'lanmagan.
2. **Biznes Qoidalar**:
   - Buyurtmada kamida bitta mahsulot bo'lishi shart.
   - Buyurtmaning umumiy summasi kamida **10.0$** bo'lishi kerak.
3. **Dependency Inversion Principle (DIP)**: `CreateOrderUseCase` to'g'ridan-to'g'ri bazaga emas, `OrderRepositoryInterface` ga bog'langan.
4. **Asinxron Ma'lumotlar Bazasi**: SQLAlchemy 2.0 va aiosqlite orqali to'liq asinxron I/O.
5. **REST API**: FastAPI va Pydantic v2 validatsiyasi bilan jihozlangan.

---

## 🚀 Ishga tushirish

### 1. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 2. FastAPI ilovasini ishga tushirish
```bash
python main.py
```
yoki:
```bash
uvicorn main:app --reload --port 8000
```

Brauzer orqali Swagger hujjatlarni ochish: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Testlarni ishga tushirish

```bash
pytest tests/
```

Barcha unit va integratsion testlar muvaffaqiyatli bajariladi.
