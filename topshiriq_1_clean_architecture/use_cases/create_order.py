from domain.models import Order, OrderItem
from domain.repository_interface import OrderRepositoryInterface


class CreateOrderUseCase:
    """
    Buyurtma yaratish biznes-mantiqi (Use Case).
    Framework va DB detallaridan butunlay mustaqil (Pure Python).
    """

    def __init__(self, repo: OrderRepositoryInterface):
        self.repo = repo

    async def execute(self, email: str, items_data: list[dict]) -> Order:
        # Biznes qoidasi 1: Kamida bitta mahsulot bo'lishi shart
        if not items_data:
            raise ValueError("Buyurtmada kamida bitta mahsulot bo'lishi shart!")

        items = [OrderItem(**item) for item in items_data]
        order = Order(id=None, customer_email=email, items=items)

        # Biznes qoidasi 2: Minimum buyurtma summasi 10.0$ bo'lishi kerak
        if order.total_price < 10.0:
            raise ValueError("Eng kam buyurtma summasi 10$ bo'lishi kerak!")

        return await self.repo.save(order)


class GetOrderUseCase:
    """
    Buyurtmani ID orqali olish biznes-mantiqi.
    """

    def __init__(self, repo: OrderRepositoryInterface):
        self.repo = repo

    async def execute(self, order_id: int) -> Order:
        order = await self.repo.get_by_id(order_id)
        if not order:
            raise ValueError(f"ID={order_id} bo'lgan buyurtma topilmadi!")
        return order
