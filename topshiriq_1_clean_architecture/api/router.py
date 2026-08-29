from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr, Field
from domain.repository_interface import OrderRepositoryInterface
from use_cases.create_order import CreateOrderUseCase, GetOrderUseCase
from infrastructure.sql_repository import get_order_repository

router = APIRouter(prefix="/orders", tags=["Orders"])


# Pydantic Request & Response Schemas
class ItemSchema(BaseModel):
    product_name: str = Field(..., description="Mahsulot nomi", min_length=1)
    price: float = Field(..., description="Mahsulot narxi ($)", gt=0)
    quantity: int = Field(..., description="Mahsulot soni", gt=0)


class CreateOrderSchema(BaseModel):
    customer_email: EmailStr = Field(..., description="Mijoz elektron pochtasi")
    items: List[ItemSchema] = Field(..., description="Buyurtma mahsulotlari ro'yxati", min_length=1)


class OrderItemResponse(BaseModel):
    product_name: str
    price: float
    quantity: int


class OrderResponse(BaseModel):
    status: str
    order_id: Optional[int] = None
    customer_email: str
    items: List[OrderItemResponse]
    total: float


class CreateOrderSuccessResponse(BaseModel):
    status: str
    order_id: Optional[int]
    total: float


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreateOrderSuccessResponse)
async def create_order(
    payload: CreateOrderSchema,
    repo: OrderRepositoryInterface = Depends(get_order_repository),
):
    """
    Yangi buyurtma yaratish endpointi.
    Clean Architecture bo'yicha Use Case'ga topshiradi.
    """
    use_case = CreateOrderUseCase(repo=repo)
    try:
        result = await use_case.execute(
            email=payload.customer_email,
            items_data=[item.model_dump() for item in payload.items],
        )
        return {
            "status": "success",
            "order_id": result.id,
            "total": result.total_price,
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    repo: OrderRepositoryInterface = Depends(get_order_repository),
):
    """ID bo'yicha buyurtma ma'lumotlarini olish."""
    use_case = GetOrderUseCase(repo=repo)
    try:
        order = await use_case.execute(order_id)
        return {
            "status": "success",
            "order_id": order.id,
            "customer_email": order.customer_email,
            "items": [
                OrderItemResponse(
                    product_name=i.product_name,
                    price=i.price,
                    quantity=i.quantity,
                )
                for i in order.items
            ],
            "total": order.total_price,
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/", response_model=List[OrderResponse])
async def list_orders(
    repo: OrderRepositoryInterface = Depends(get_order_repository),
):
    """Barcha buyurtmalar ro'yxati."""
    orders = await repo.get_all()
    return [
        OrderResponse(
            status="success",
            order_id=o.id,
            customer_email=o.customer_email,
            items=[
                OrderItemResponse(
                    product_name=i.product_name,
                    price=i.price,
                    quantity=i.quantity,
                )
                for i in o.items
            ],
            total=o.total_price,
        )
        for o in orders
    ]
