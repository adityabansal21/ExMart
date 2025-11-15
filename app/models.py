from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Supplier(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    company_name: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    products: List["Product"] = Relationship(back_populates="supplier")


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    price_from: Optional[float] = None
    price_to: Optional[float] = None
    images: Optional[str] = None  # comma-separated URLs for starter
    supplier_id: Optional[int] = Field(default=None, foreign_key="supplier.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    supplier: Optional[Supplier] = Relationship(back_populates="products")


class Enquiry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int
    buyer_name: str
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
