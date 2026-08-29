from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.database import init_db
from api.router import router as orders_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ma'lumotlar bazasidagi jadvallarni tekshirish va yaratish
    await init_db()
    yield
    # Shutdown: resurslarni yopish kerak bo'lsa shu yerda


app = FastAPI(
    title="Clean Architecture E-Commerce Order Service API",
    description="1-Topshiriq: Clean Architecture asosida qurilgan buyurtmalarni boshqarish xizmati.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS sozlamalari
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routerlarni ulash
app.include_router(orders_router)


@app.get("/")
async def root():
    return {
        "message": "Clean Architecture Order Service ishlamoqda!",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
