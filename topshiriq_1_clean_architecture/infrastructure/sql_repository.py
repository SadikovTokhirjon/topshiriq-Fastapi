from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models import Order, OrderItem
from domain.repository_interface import OrderRepositoryInterface
from infrastructure.db_models import OrderDB, OrderItemDB
from infrastructure.database import AsyncSessionLocal


class SQLAlchemyOrderRepository(OrderRepositoryInterface):
    """
    SQLAlchemy orqali ma'lumotlar bazasi bilan ishlovchi repository.
    Domain Entity va DB Model o'rtasidagi konvertatsiyani amalga oshiradi.
    """

    def __init__(self, session: Optional[AsyncSession] = None):
        self.session = session

    async def save(self, order: Order) -> Order:
        """Domain Order obyektini bazaga yozish va qaytarish."""
        if self.session:
            return await self._save_with_session(self.session, order)

        async with AsyncSessionLocal() as session:
            return await self._save_with_session(session, order)

    async def _save_with_session(self, session: AsyncSession, order: Order) -> Order:
        # Domain Entity -> Database Model
        db_order = OrderDB(customer_email=order.customer_email)
        for item in order.items:
            db_item = OrderItemDB(
                product_name=item.product_name,
                price=item.price,
                quantity=item.quantity,
            )
            db_order.items.append(db_item)

        session.add(db_order)
        await session.commit()
        await session.refresh(db_order)

        # Database Model -> Domain Entity
        saved_items = [
            OrderItem(
                product_name=it.product_name,
                price=it.price,
                quantity=it.quantity,
            )
            for it in db_order.items
        ]
        return Order(
            id=db_order.id,
            customer_email=db_order.customer_email,
            items=saved_items,
        )

    async def get_by_id(self, order_id: int) -> Optional[Order]:
        """ID bo'yicha buyurtmani olish."""
        if self.session:
            return await self._get_by_id_with_session(self.session, order_id)

        async with AsyncSessionLocal() as session:
            return await self._get_by_id_with_session(session, order_id)

    async def _get_by_id_with_session(self, session: AsyncSession, order_id: int) -> Optional[Order]:
        stmt = select(OrderDB).where(OrderDB.id == order_id)
        result = await session.execute(stmt)
        db_order = result.scalar_one_or_none()

        if not db_order:
            return None

        saved_items = [
            OrderItem(
                product_name=it.product_name,
                price=it.price,
                quantity=it.quantity,
            )
            for it in db_order.items
        ]
        return Order(
            id=db_order.id,
            customer_email=db_order.customer_email,
            items=saved_items,
        )

    async def get_all(self) -> List[Order]:
        """Barcha buyurtmalarni olish."""
        async with AsyncSessionLocal() as session:
            stmt = select(OrderDB)
            result = await session.execute(stmt)
            db_orders = result.scalars().all()

            orders = []
            for db_order in db_orders:
                items = [
                    OrderItem(
                        product_name=it.product_name,
                        price=it.price,
                        quantity=it.quantity,
                    )
                    for it in db_order.items
                ]
                orders.append(
                    Order(
                        id=db_order.id,
                        customer_email=db_order.customer_email,
                        items=items,
                    )
                )
            return orders


def get_order_repository() -> OrderRepositoryInterface:
    """FastAPI Dependency Injection uchun provayder."""
    return SQLAlchemyOrderRepository()
