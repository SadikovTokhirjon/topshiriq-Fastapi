from typing import List, Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# 1. Database Model sozlamalari
class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    # 1:N Bog'lanish: Bitta kategoriyada ko'plab mahsulotlar bo'lishi mumkin
    products: Mapped[List["Product"]] = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # SQL Index tezlashtirish uchun (WHERE name = '...')
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    # Foreign Key va Index (JOIN va WHERE category_id = ... so'rovlarini tezlashtirish uchun)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), index=True, nullable=False)

    # N:1 Bog'lanish
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="products")
