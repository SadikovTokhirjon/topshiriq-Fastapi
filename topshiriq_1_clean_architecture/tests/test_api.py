import pytest
from fastapi.testclient import TestClient
from main import app
from infrastructure.sql_repository import get_order_repository
from domain.models import Order, OrderItem
from domain.repository_interface import OrderRepositoryInterface


class MockRepository(OrderRepositoryInterface):
    def __init__(self):
        self.orders = {}
        self.counter = 1

    async def save(self, order: Order) -> Order:
        order_id = self.counter
        self.counter += 1
        saved = Order(id=order_id, customer_email=order.customer_email, items=order.items)
        self.orders[order_id] = saved
        return saved

    async def get_by_id(self, order_id: int):
        return self.orders.get(order_id)

    async def get_all(self):
        return list(self.orders.values())


mock_repo = MockRepository()


def override_get_order_repository():
    return mock_repo


app.dependency_overrides[get_order_repository] = override_get_order_repository
client = TestClient(app)


def test_api_create_order_success():
    payload = {
        "customer_email": "client@example.com",
        "items": [
            {"product_name": "Laptop stand", "price": 30.0, "quantity": 1},
            {"product_name": "USB Cable", "price": 5.0, "quantity": 2},
        ],
    }
    response = client.post("/orders/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["total"] == 40.0
    assert data["order_id"] is not None


def test_api_create_order_below_minimum_price():
    payload = {
        "customer_email": "client@example.com",
        "items": [
            {"product_name": "Sticker", "price": 2.0, "quantity": 1},
        ],
    }
    response = client.post("/orders/", json=payload)
    assert response.status_code == 400
    assert "Eng kam buyurtma summasi" in response.json()["detail"]


def test_api_get_order_by_id():
    # Avval buyurtma yaratamiz
    create_payload = {
        "customer_email": "buyer@test.com",
        "items": [{"product_name": "Keyboard", "price": 50.0, "quantity": 1}],
    }
    create_res = client.post("/orders/", json=create_payload)
    order_id = create_res.json()["order_id"]

    # ID bo'yicha olamiz
    get_res = client.get(f"/orders/{order_id}")
    assert get_res.status_code == 200
    data = get_res.json()
    assert data["order_id"] == order_id
    assert data["customer_email"] == "buyer@test.com"
    assert data["total"] == 50.0
    assert len(data["items"]) == 1
