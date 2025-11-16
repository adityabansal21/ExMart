from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from . import crud, models
from typing import Optional
from fastapi import UploadFile, File
from pathlib import Path

app = FastAPI(title="B2B Marketplace - Starter")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize DB & seed
crud.init_db()
crud.seed_if_empty()

# REST API endpoints
@app.get("/api/products")
def api_list_products(q: Optional[str] = None, limit: int = 20, offset: int = 0):
    items = crud.list_products(q=q, limit=limit, offset=offset)
    return {"items": [p.dict() for p in items]}

@app.get("/api/products/{product_id}")
def api_get_product(product_id: int):
    p = crud.get_product(product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return p

@app.post("/api/enquiries")
async def api_create_enquiry(product_id: int = Form(...), buyer_name: str = Form(...), message: str = Form(...)):
    e = crud.create_enquiry(product_id=product_id, buyer_name=buyer_name, message=message)
    # In production: send notification/email to supplier here
    return {"status":"ok", "enquiry_id": e.id}

# Simple web UI routes (server-rendered)
@app.get("/", response_class=HTMLResponse)
def index(request: Request, q: Optional[str]=None):
    products = crud.list_products(q=q)
    return templates.TemplateResponse("index.html", {"request": request, "products": products, "q": q or ""})

@app.get("/product/{product_id}", response_class=HTMLResponse)
def product_detail(request: Request, product_id: int):
    p = crud.get_product(product_id)
    if not p:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("product.html", {"request": request, "product": p})

@app.post("/enquire")
def enquire(product_id: int = Form(...), buyer_name: str = Form(...), message: str = Form(...)):
    e = crud.create_enquiry(product_id=product_id, buyer_name=buyer_name, message=message)
    return RedirectResponse(url=f"/product/{product_id}?sent=1", status_code=303)


@app.get("/supplier/onboard", response_class=HTMLResponse)
def supplier_onboard_form(request: Request):
    return templates.TemplateResponse("supplier_onboard.html", {"request": request})

@app.post("/supplier/onboard")
async def supplier_onboard_submit(
    request: Request,
    company_name: str = Form(None),
    brand_name: str = Form(None),
    business_type: str = Form(None),
    industry_category: str = Form(None),
    year_of_establishment: str = Form(None),

    contact_person: str = Form(None),
    designation: str = Form(None),
    mobile_number: str = Form(None),
    alt_mobile_number: str = Form(None),
    email: str = Form(None),

    registered_address: str = Form(None),
    state: str = Form(None),
    district: str = Form(None),
    pincode: str = Form(None),
    google_map_location: str = Form(None),

    gst_number: str = Form(None),
    udysm_msme: str = Form(None),
    pam_number: str = Form(None),
    pbu_category: str = Form(None),
    num_employees: str = Form(None),

    description: str = Form(None),
    key_products: str = Form(None),
    intro_video: str = Form(None),

    banner_image: UploadFile = File(None),
    catalog_pdf: UploadFile = File(None),
):
    # save files (if present)
    banner_path = None
    catalog_path = None
    if banner_image:
        banner_path = save_upload_file(banner_image)  # returns relative path like static/uploads/abcd.png
    if catalog_pdf:
        catalog_path = save_upload_file(catalog_pdf)

    company_data = {
        "company_name": company_name,
        "brand_name": brand_name,
        "business_type": business_type,
        "industry_category": industry_category,
        "year_of_establishment": year_of_establishment,
        "contact_person": contact_person,
        "designation": designation,
        "mobile_number": mobile_number,
        "alt_mobile_number": alt_mobile_number,
        "email": email,
        "registered_address": registered_address,
        "state": state,
        "district": district,
        "pincode": pincode,
        "google_map_location": google_map_location,
        "gst_number": gst_number,
        "udysm_msme": udysm_msme,
        "pam_number": pam_number,
        "pbu_category": pbu_category,
        "num_employees": num_employees,
        "description": description,
        "key_products": key_products,
        "intro_video": intro_video,
    }

    cp = create_company_profile(company_data, banner_filename=banner_path, catalog_filename=catalog_path)
    # redirect to a confirmation or preview page
    return RedirectResponse(url=f"/supplier/onboard?submitted=1&id={cp.id}", status_code=303)

