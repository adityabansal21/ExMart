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


class CompanyProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company_name: Optional[str] = None
    brand_name: Optional[str] = None
    business_type: Optional[str] = None
    industry_category: Optional[str] = None
    year_of_establishment: Optional[str] = None

    contact_person: Optional[str] = None
    designation: Optional[str] = None
    mobile_number: Optional[str] = None
    alt_mobile_number: Optional[str] = None
    email: Optional[str] = None

    registered_address: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    pincode: Optional[str] = None
    google_map_location: Optional[str] = None

    gst_number: Optional[str] = None
    udysm_msme: Optional[str] = None
    pam_number: Optional[str] = None
    pbu_category: Optional[str] = None
    num_employees: Optional[str] = None

    description: Optional[str] = None
    key_products: Optional[str] = None
    intro_video: Optional[str] = None

    banner_image_path: Optional[str] = None
    catalog_pdf_path: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
