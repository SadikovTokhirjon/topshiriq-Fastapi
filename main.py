import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Sub-loyihalar yo'lini qo'shamiz
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "topshiriq_1_clean_architecture")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "topshiriq_3_database_optimization_redis")))

# 1-Topshiriq importlari
from topshiriq_1_clean_architecture.infrastructure.database import init_db as init_orders_db
from topshiriq_1_clean_architecture.api.router import router as orders_router

# 3-Topshiriq importlari
from topshiriq_3_database_optimization_redis.database import init_db as init_catalog_db
from topshiriq_3_database_optimization_redis.catalog_service import CatalogService
from topshiriq_3_database_optimization_redis.main import app as catalog_app


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ikkala modulning ma'lumotlar bazasini asinxron initsializatsiya qilamiz
    await init_orders_db()
    await init_catalog_db()
    yield


app = FastAPI(
    title="Modern Python Back-end & High Performance Unified API",
    description=(
        "Ushbu loyiha 1-topshiriq (Clean Architecture Order Service) va "
        "3-topshiriq (Database Optimization & Redis Cache-Aside) ni bitta umumiy platformaga birlashtiradi."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1-Topshiriq routerini ulash
app.include_router(orders_router)

# 3-Topshiriq routerlarini ulash
for route in catalog_app.routes:
    if getattr(route, "path", "").startswith("/products"):
        app.routes.append(route)


@app.get("/")
async def root():
    return {
        "message": "Modern Python Back-end Birlashtirilgan Loyiha ishlamoqda!",
        "topshiriq_1_orders": "/orders/",
        "topshiriq_3_products": "/products/",
        "swagger_docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
