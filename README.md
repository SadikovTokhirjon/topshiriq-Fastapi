# Modern Python Back-end and High Performance Topshiriqlari

Ushbu repositoryda Notion darsligi asosida berilgan 1-topshiriq va 3-topshiriq to'liq alohida papkalarga ajratilgan holda bajarilgan:

---

## 📁 Loyihalar Strukturasi

```
topshiriq/
├── venv/                                     # Virtual muhit
├── requirements.txt                          # Loyiha umumiy bog'liqliklari
├── README.md                                 # Umumiy qo'llanma
│
├── topshiriq_1_clean_architecture/           # 1-TOPShIRIQ: Clean Architecture E-Commerce API
│   ├── domain/                               # Domain qatlami (Order, OrderItem, RepositoryInterface)
│   │   ├── models.py
│   │   └── repository_interface.py
│   ├── use_cases/                            # Use Cases qatlami (CreateOrder, GetOrder)
│   │   └── create_order.py
│   ├── infrastructure/                       # Infrastructure qatlami (SQLAlchemy, SQLite, Repositories)
│   │   ├── database.py
│   │   ├── db_models.py
│   │   └── sql_repository.py
│   ├── api/                                  # Interface Adapters (FastAPI REST Controller)
│   │   └── router.py
│   ├── tests/                                # Unit va integratsiya testlari
│   │   ├── test_use_cases.py
│   │   └── test_api.py
│   ├── main.py                               # FastAPI ilovasi
│   ├── README.md                             # 1-topshiriq bo'yicha batafsil qo'llanma
│   └── requirements.txt
│
└── topshiriq_3_database_optimization_redis/  # 3-TOPShIRIQ: DB Optimizatsiya va Redis Cache-Aside
    ├── models.py                             # Category va Product modellari (SQL Index)
    ├── database.py                           # Async SQLite DB va dastlabki seed ma'lumotlar
    ├── redis_client.py                       # Redis Async Client (Haqiqiy Redis va InMemory fallback)
    ├── catalog_service.py                    # Cache-Aside, TTL 300s, Invalidation, joinedload
    ├── explain_analysis.py                   # SQL EXPLAIN QUERY PLAN tahlil skripti
    ├── demo.py                               # Interaktiv demo namoyish skripti
    ├── main.py                               # FastAPI REST API
    ├── tests/                                # Kesh va optimizatsiya testlari
    │   └── test_catalog_service.py
    ├── README.md                             # 3-topshiriq bo'yicha batafsil qo'llanma
    └── requirements.txt
```

---

## 🚀 Virtual Muhitni faollashtirish va Ishga tushirish

### 1. Virtual muhitni faollashtirish (Windows PowerShell):
```powershell
.\venv\Scripts\Activate.ps1
```
yoki (CMD):
```cmd
venv\Scripts\activate.bat
```

### 2. Kutubxonalarni o'rnatish:
```bash
pip install -r requirements.txt
```

---

## 📌 1-Topshiriqni ishga tushirish (Clean Architecture):
```bash
cd topshiriq_1_clean_architecture
python main.py
```
- Swagger API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Testlarni ishga tushirish: `pytest tests/`

---

## 📌 3-Topshiriqni ishga tushirish (Database Optimization & Redis):
```bash
cd topshiriq_3_database_optimization_redis
python demo.py             # Interaktiv konsol demosi
python explain_analysis.py # SQL Indeks va Explain tahlili
python main.py             # FastAPI REST API (Port: 8001)
```
- Swagger API Docs: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)
- Testlarni ishga tushirish: `pytest tests/`
