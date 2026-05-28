# from fastapi import FastAPI



# @app.get("/", tags=["Root"])
# async def root():
#     """Entry point của API."""
#     return {"message": "Hello", "version": "1.0"}

from fastapi import FastAPI, Path, Query, HTTPException
app = FastAPI(title="Demo API", version="1.0.0")
fake_products = {i: {"id": i, "name": f"Product {i}"} for i in range(1, 101)}

@app.get("/products/{product_id}", tags=["Products"])
async def get_product(
    product_id: int = Path(gt=0, description="ID sản phẩm"),
):
    if product_id not in fake_products:
        raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")
    return fake_products[product_id]

@app.get("/products", tags=["Products"])
async def list_products(
    skip:   int       = Query(default=0,    ge=0),
    limit:  int       = Query(default=10,   ge=1, le=50),
    search: str | None = Query(default=None, min_length=1),
):
    items = list(fake_products.values())
    if search:
        items = [p for p in items if search.lower() in p["name"].lower()]
    return {"total": len(items), "data": items[skip: skip + limit]}

from datetime import datetime
from pydantic import BaseModel, Field
app = FastAPI(title="Demo API", version="1.0.0")

class ProductCreate(BaseModel):
    name:  str   = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)
    stock: int   = Field(ge=0, default=0)

class ProductResponse(BaseModel):
    id:         int
    name:       str
    price:      float
    stock:      int
    created_at: datetime

class ProductUpdate(BaseModel):
    name:  str | None   = Field(None, min_length=2, max_length=100)
    price: float | None = Field(None, gt=0)
    stock: int | None   = Field(None, ge=0)

product_db: dict[int, dict] = {}
_counter = 0

@app.post("/products", response_model=ProductResponse, status_code=201, tags=["Products"])
async def create_product(product: ProductCreate):
    global _counter
    _counter += 1
    new = {
        "id": _counter,
        "created_at": datetime.now(),
        **product.model_dump(),
    }
    product_db[_counter] = new
    return new

@app.patch("/products/{id}", response_model=ProductResponse, tags=["Products"])
async def update_product(id: int, product: ProductUpdate):
    if id not in product_db:
        raise HTTPException(status_code=404, detail="Không tìm thấy")
    update_data = product.model_dump(exclude_unset=True)  # chỉ field đã set
    product_db[id].update(update_data)
    return product_db[id]