import pytest
from domain.models import Order, OrderItem
from domain.repository_interface import OrderRepositoryInterface
from use_cases.create_order import CreateOrderUseCase, GetOrderUseCase


class FakeOrderRepository(OrderRepositoryInterface):
    """Clean Architecture: Testlar uchun DBsiz mustaqil Mock/Fake Repository."""

    def __init__(self):
        self.orders: dict[int, Order] = {}
        self._current_id = 1

    async def save(self, order: Order) -> Order:
        order_id = self._current_id
        self._current_id += 1
        saved_order = Order(
            id=order_id,
            customer_email=order.customer_email,
            items=order.items,
        )
        self.orders[order_id] = saved_order
        return saved_order

    async def get_by_id(self, order_id: int) -> Order | None:
        return self.orders.get(order_id)

    async def get_all(self) -> list[Order]:
        return list(self.orders.values())


@pytest.mark.asyncio
async def test_create_order_success():
    repo = FakeOrderRepository()
    use_case = CreateOrderUseCase(repo=repo)

    items = [
        {"product_name": "Keyboard", "price": 25.0, "quantity": 1},
        {"product_name": "Mouse", "price": 15.0, "quantity": 2},
    ]
    order = await use_case.execute(email="user@example.com", items_data=items)

    assert order.id is not None
    assert order.id == 1
    assert order.customer_email == "user@example.com"
    assert len(order.items) == 2
    assert order.total_price == 55.0  # 25 + (15*2)


@pytest.mark.asyncio
async def test_create_order_empty_items_error():
    repo = FakeOrderRepository()
    use_case = CreateOrderUseCase(repo=repo)

    with pytest.raises(ValueError, match="kamida bitta mahsulot bo'lishi shart"):
        await use_case.execute(email="user@example.com", items_data=[])


@pytest.mark.asyncio
async def test_create_order_minimum_price_error():
    repo = FakeOrderRepository()
    use_case = CreateOrderUseCase(repo=repo)

    # Total = 5.0 < 10.0
    items = [{"product_name": "Pen", "price": 2.5, "quantity": 2}]
    with pytest.raises(ValueError, match="Eng kam buyurtma summasi 10$ bo'lishi kerak"):
        await use_case.execute(email="user@example.com", items_data=items)


@pytest.mark.asyncio
async def test_get_order_use_case():
    repo = FakeOrderRepository()
    create_uc = CreateOrderUseCase(repo=repo)
    get_uc = GetOrderUseCase(repo=repo)

    created = await create_uc.execute(
        email="test@mail.com",
        items_data=[{"product_name": "Monitor", "price": 200.0, "quantity": 1}],
    )

    fetched = await get_uc.execute(created.id)
    assert fetched.id == created.id
    assert fetched.customer_email == "test@mail.com"
    assert fetched.total_price == 200.0


@pytest.mark.asyncio
async def test_get_non_existent_order_raises_error():
    repo = FakeOrderRepository()
    get_uc = GetOrderUseCase(repo=repo)

    with pytest.raises(ValueError, match="topilmadi"):
        await get_uc.execute(999)
