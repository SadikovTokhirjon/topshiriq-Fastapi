from dataclasses import dataclass, field
from typing import List


@dataclass
class OrderItem:
    product_name: str
    price: float
    quantity: int


@dataclass
class Order:
    id: int | None
    customer_email: str
    items: List[OrderItem] = field(default_factory=list)

    @property
    def total_price(self) -> float:
        return sum(item.price * item.quantity for item in self.items)
