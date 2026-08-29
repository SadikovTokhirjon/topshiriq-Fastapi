from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models import Order


class OrderRepositoryInterface(ABC):
    """
    Clean Architecture Repository interfeysi (Dependency Inversion Principle).
    Biznes qatlam (Domain / Use Cases) tashqi ma'lumotlar bazasiga to'g'ridan-to'g'ri bog'lanmaydi.
    """

    @abstractmethod
    async def save(self, order: Order) -> Order:
        """Buyurtmani saqlaydi va id bilan qaytaradi."""
        pass

    @abstractmethod
    async def get_by_id(self, order_id: int) -> Optional[Order]:
        """ID bo'yicha buyurtmani qaytaradi."""
        pass

    @abstractmethod
    async def get_all(self) -> List[Order]:
        """Barcha buyurtmalar ro'yxatini qaytaradi."""
        pass
