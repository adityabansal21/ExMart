from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from . import crud, models
from typing import Optional

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
