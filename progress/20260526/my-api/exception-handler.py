# ============================================================
# Bài 1 — Hello World + Swagger
# ============================================================

from fastapi import FastAPI

app = FastAPI(title="Demo API", version="1.0.0")

@app.get("/", tags=["Root"])
async def root():
    """Entry point của API."""
    return {"message": "Hello", "version": "1.0"}

# Chạy: uvicorn main:app --reload → mở /docs → test Try it out


# ============================================================
# Bài 2 — Path + Query params có validation
# ============================================================

from fastapi import FastAPI, Path, Query, HTTPException

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

# Test: GET /products?limit=200  → 422
# Test: GET /products/0          → 422


# ============================================================
# Bài 3 — POST với Request Body + Response Model
# ============================================================

from pydantic import BaseModel, Field
from datetime import datetime

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


# ============================================================
# Bài 4 — HTTPException + Custom Exception Handler
# ============================================================

from fastapi import Request
from fastapi.responses import JSONResponse

class DuplicateError(Exception):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value

@app.exception_handler(DuplicateError)
async def duplicate_handler(request: Request, exc: DuplicateError):
    return JSONResponse(
        status_code=409,
        content={
            "code": "DUPLICATE",
            "field": exc.field,
            "message": f"Giá trị '{exc.value}' đã tồn tại",
        },
    )

@app.post("/products/strict", response_model=ProductResponse, status_code=201, tags=["Products"])
async def create_product_strict(product: ProductCreate):
    # Kiểm tra tên trùng
    for p in product_db.values():
        if p["name"].lower() == product.name.lower():
            raise DuplicateError("name", product.name)
    # Tạo mới...
    global _counter
    _counter += 1
    new = {"id": _counter, "created_at": datetime.now(), **product.model_dump()}
    product_db[_counter] = new
    return new


# ============================================================
# Bài 5 — Mini CRUD API hoàn chỉnh
# ============================================================

from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI(title="Product CRUD API", version="1.0.0")

# --- Schemas ---
class ProductCreate(BaseModel):
    name:  str   = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)
    stock: int   = Field(ge=0, default=0)

class ProductUpdate(BaseModel):
    name:  str | None   = Field(None, min_length=2)
    price: float | None = Field(None, gt=0)
    stock: int | None   = Field(None, ge=0)

class ProductResponse(BaseModel):
    id:    int
    name:  str
    price: float
    stock: int

# --- In-memory store ---
_db: dict[int, dict] = {}
_next_id = 1

# --- Endpoints ---
@app.get("/products", response_model=list[ProductResponse], tags=["Products"])
async def list_products(
    skip:  int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
):
    items = list(_db.values())
    return items[skip: skip + limit]

@app.get("/products/{id}", response_model=ProductResponse, tags=["Products"])
async def get_product(id: int = Path(gt=0)):
    if id not in _db:
        raise HTTPException(status_code=404, detail=f"Product {id} không tồn tại")
    return _db[id]

@app.post("/products", response_model=ProductResponse,
          status_code=status.HTTP_201_CREATED, tags=["Products"])
async def create_product(product: ProductCreate):
    global _next_id
    item = {"id": _next_id, **product.model_dump()}
    _db[_next_id] = item
    _next_id += 1
    return item

@app.patch("/products/{id}", response_model=ProductResponse, tags=["Products"])
async def update_product(id: int, product: ProductUpdate):
    if id not in _db:
        raise HTTPException(status_code=404, detail=f"Product {id} không tồn tại")
    _db[id].update(product.model_dump(exclude_unset=True))
    return _db[id]

@app.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Products"])
async def delete_product(id: int):
    if id not in _db:
        raise HTTPException(status_code=404, detail=f"Product {id} không tồn tại")
    del _db[id]
    # Không return gì → 204 No Content

# Chạy: uvicorn main:app --reload
# Test toàn bộ tại: http://localhost:8000/docs