import os
from sqlmodel import Session, select
from .models import Product, Supplier, Enquiry, CompanyProfile
from sqlmodel import SQLModel, create_engine
from typing import List, Optional
from . import crud  # existing import style


engine = create_engine("sqlite:///./db.sqlite", echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)

# Seed simple data
def seed_if_empty():
    with get_session() as s:
        products = s.exec(select(Product)).all()
        if products:
            return
        sup = Supplier(name="ACME Traders", company_name="ACME Pvt Ltd", phone="9876543210")
        s.add(sup); s.commit(); s.refresh(sup)
        p1 = Product(title="Industrial Bolt M8", description="Hex bolt – pack of 100", price_from=500, price_to=800, images="", supplier_id=sup.id)
        p2 = Product(title="Stainless Steel Tubing", description="304 grade tubing", price_from=2000, price_to=5000, images="", supplier_id=sup.id)
        s.add_all([p1,p2])
        s.commit()

def list_products(q: Optional[str]=None, limit: int=20, offset: int=0) -> List[Product]:
    with get_session() as s:
        stmt = select(Product)
        if q:
            qlike = f"%{q}%"
            stmt = select(Product).where((Product.title.ilike(qlike)) | (Product.description.ilike(qlike)))
        stmt = stmt.offset(offset).limit(limit)
        return s.exec(stmt).all()

def get_product(product_id:int) -> Optional[Product]:
    with get_session() as s:
        return s.get(Product, product_id)

def create_enquiry(product_id:int, buyer_name:str, message:str) -> Enquiry:
    with get_session() as s:
        e = Enquiry(product_id=product_id, buyer_name=buyer_name, message=message)
        s.add(e); s.commit(); s.refresh(e)
        return e

UPLOAD_DIR = "static/uploads"

def create_company_profile(
    company_data: dict,
    banner_filename: Optional[str] = None,
    catalog_filename: Optional[str] = None
) -> CompanyProfile:
    # company_data is a dict with keys matching CompanyProfile fields
    with get_session() as s:
        cp = CompanyProfile(**company_data)
        if banner_filename:
            cp.banner_image_path = banner_filename
        if catalog_filename:
            cp.catalog_pdf_path = catalog_filename
        s.add(cp)
        s.commit()
        s.refresh(cp)
        return cp
