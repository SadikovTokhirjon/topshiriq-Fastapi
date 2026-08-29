from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from database import init_db
from catalog_service import CatalogService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield


app = FastAPI(
    title="Database Optimization & Redis Cache-Aside Service",
    description="3-Topshiriq: SQL Index, N+1 muammosi yechimi va Redis Cache-Aside Pattern API.",
    version="1.0.0",
    lifespan=lifespan,
)


class UpdatePriceSchema(BaseModel):
    new_price: float = Field(..., gt=0, description="Yangi mahsulot narxi ($)")


class CategoryOut(BaseModel):
    id: Optional[int]
    name: Optional[str]


class ProductDetailOut(BaseModel):
    id: int
    name: str
    price: float
    category_id: int


class ProductWithCategoryOut(BaseModel):
    id: int
    name: str
    price: float
    category: CategoryOut


@app.get("/")
async def root():
    return {
        "message": "Database Optimization & Redis Cache-Aside Service ishlamoqda!",
        "docs": "/docs",
    }


@app.get("/products/{product_id}", response_model=ProductDetailOut)
async def get_product(product_id: int):
    """
    Redis Cache-Aside Pattern orqali mahsulotni olish.
    Keshda bo'lsa darhol qaytaradi, bo'lmasa DB'dan olib keshga yozadi.
    """
    product = await CatalogService.get_product_detail(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID={product_id} bo'lgan mahsulot topilmadi!",
        )
    return product


@app.put("/products/{product_id}/price", response_model=ProductDetailOut)
async def update_price(product_id: int, payload: UpdatePriceSchema):
    """
    Mahsulot narxini yangilash va keshni tozalash (Cache Invalidation).
    """
    updated = await CatalogService.update_product_price(product_id, payload.new_price)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID={product_id} bo'lgan mahsulot topilmadi!",
        )
    return updated


@app.get("/products/", response_model=List[ProductWithCategoryOut])
async def list_products():
    """
    N+1 muammosisiz (joinedload orqali 1 ta so'rovda) barcha mahsulotlar va kategoriyalar.
    """
    return await CatalogService.get_products_with_category_optimized()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
