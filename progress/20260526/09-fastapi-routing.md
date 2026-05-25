# 09 — FastAPI Cơ Bản & Routing

> **Khối 9 — Làm Quen FastAPI & Routing**
> Dành cho Java developer — tập trung vào điểm khác biệt so với Spring Boot.

---

## A — FastAPI Là Gì? Tại Sao Dùng?

### A.1 WHAT — FastAPI là gì?

- Web framework Python để xây REST API — tương tự **Spring Boot** (Java)
- Xây trên **Starlette** (ASGI) + **Pydantic** (validation)
- ASGI = Asynchronous Server Gateway Interface → hỗ trợ `async/await` native
- Phiên bản: FastAPI 0.136+ | Python 3.12+

### A.2 WHY — Tại sao chọn FastAPI?

- Tự động sinh **Swagger UI `/docs`** + **ReDoc `/redoc`** từ code — không cần config
- Validation request/response tự động qua Pydantic — không viết thêm code
- Native `async/await` — xử lý concurrent I/O hiệu quả
- Hiệu năng ngang Node.js/Go — cao hơn Flask ~3x, Django ~5x
- Type hints = documentation = validation = editor autocomplete **cùng lúc**

### A.3 So sánh Flask / Django / FastAPI

| | Flask | Django | FastAPI |
|--|-------|--------|---------|
| Định hướng | Micro, linh hoạt | Full-stack (ORM+template+admin) | API-focused |
| Async | Không native | Không native | **Native** |
| Validation | Tự làm | Form/DRF | **Pydantic tự động** |
| Docs | Không có | Không có | **/docs tự động** |

### A.4 ⚠️ Java vs FastAPI — Đối chiếu trực tiếp

| Spring Boot | FastAPI |
|-------------|---------|
| `@RestController` | `app = FastAPI()` (không cần class) |
| `@GetMapping('/users')` | `@app.get('/users')` |
| `@RequestBody @Valid UserDTO` | `user: UserCreate` (Pydantic tự validate) |
| `@PathVariable Long id` | `id: int` (tên trùng `{id}` trong path) |
| `@RequestParam int page` | `page: int = 0` (có default = query param) |
| Springfox/SpringDoc dependency | `/docs` `/redoc` có sẵn, không cần config |
| Tomcat (WSGI-like) | Uvicorn (ASGI) |

---

## B — Cài Đặt & Hello World

### B.1 Cài đặt (khuyến khích dùng uv)

```bash
# Dùng uv (khuyến khích)
uv init my-api && cd my-api
uv add fastapi uvicorn[standard] pydantic-settings
uv add --dev httpx pytest ruff mypy

# Hoặc pip
pip install fastapi uvicorn[standard]
# uvicorn[standard] → cài thêm: websockets, httptools, python-dotenv
```

### B.2 Hello World

```python
# main.py
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    version="1.0.0",
    description="API demo cho Java developer",
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### B.3 Chạy server

```bash
uvicorn main:app --reload
# main      = tên file main.py
# app       = tên biến FastAPI()
# --reload  = auto restart khi sửa code (dev only)
# Mặc định: http://localhost:8000

uv run uvicorn main:app --reload   # nếu dùng uv
```

### B.4 Kiểm tra ngay sau khi chạy

| URL | Nội dung |
|-----|----------|
| `http://localhost:8000` | API endpoint |
| `http://localhost:8000/docs` | **Swagger UI — tự động!** |
| `http://localhost:8000/redoc` | **ReDoc — tự động!** |
| `http://localhost:8000/openapi.json` | JSON schema — tự động! |

### B.5 FastAPI() constructor options

```python
app = FastAPI(
    title="Product API",
    description="API quản lý sản phẩm",
    version="1.0.0",
    docs_url="/docs",           # đổi URL Swagger (None = tắt)
    redoc_url="/redoc",         # None = tắt ReDoc
    openapi_url="/openapi.json",
)
```

---

## C — Swagger UI (/docs) & ReDoc (/redoc)

### C.1 FastAPI tự sinh docs từ đâu?

FastAPI đọc toàn bộ thông tin từ code của bạn:

```
type hints tham số  → sinh schema cho params
Pydantic model      → sinh request/response schema
docstring function  → sinh description
decorator @app.get  → sinh HTTP method + path
```

### C.2 Thêm metadata cho endpoint

```python
@app.get(
    "/users/{id}",
    summary="Lấy thông tin user",
    description="Trả về chi tiết user theo ID. 404 nếu không tìm thấy.",
    response_description="User object đầy đủ",
    tags=["Users"],          # nhóm trong Swagger UI
    deprecated=False,
)
async def get_user(id: int):
    """
    Docstring cũng hiển thị trong /docs.

    - **id**: ID của user, phải là số nguyên dương
    """
    ...
```

### C.3 Tags để nhóm endpoint

```python
@app.get("/users",    tags=["Users"])
@app.post("/users",   tags=["Users"])
@app.get("/products", tags=["Products"])

# Khai báo metadata cho tag
app = FastAPI(openapi_tags=[
    {"name": "Users",    "description": "Quản lý người dùng"},
    {"name": "Products", "description": "Quản lý sản phẩm"},
])
```

### C.4 ⚠️ Tắt docs trong production

```python
import os

app = FastAPI(
    docs_url="/docs"  if os.getenv("ENV") != "production" else None,
    redoc_url="/redoc" if os.getenv("ENV") != "production" else None,
)
```

---

## D — Path Operations — @app.get/post/put/delete

### D.1 Các HTTP method

```python
@app.get("/users")          # GET    /users      → list
@app.post("/users")         # POST   /users      → tạo mới
@app.get("/users/{id}")     # GET    /users/123  → lấy 1
@app.put("/users/{id}")     # PUT    /users/123  → replace toàn bộ
@app.patch("/users/{id}")   # PATCH  /users/123  → update một phần
@app.delete("/users/{id}")  # DELETE /users/123  → xóa
```

### D.2 async def vs def — khi nào dùng gì?

```python
# async def → khi có await bên trong (gọi DB, HTTP)
@app.get("/users/{id}")
async def get_user(id: int):
    user = await db.fetch_one(id)   # await async DB
    return user

# def → FastAPI tự chạy trong thread pool (an toàn với blocking code)
@app.get("/config")
def get_config():
    return {"version": "1.0"}       # không có I/O → def là đủ
```

> ⚠️ **ĐỪNG** dùng `requests` (sync) trong `async def` → block event loop toàn bộ server!
> ✅ Dùng `httpx.AsyncClient()` trong `async def`

### D.3 Return value → tự động JSON

```python
return {"key": "value"}   # → JSON object
return [1, 2, 3]          # → JSON array
return "hello"            # → JSON string "hello"
return user_pydantic_obj  # → FastAPI dùng response_model serialize
# FastAPI tự set Content-Type: application/json
```

### D.4 ⚠️ Thứ tự route — QUAN TRỌNG

```python
# ✅ ĐÚNG — /users/me khai báo TRƯỚC /users/{id}
@app.get("/users/me")       # match trước
@app.get("/users/{id}")     # match sau

# ❌ SAI — 'me' bị hiểu là {id} = 'me'
@app.get("/users/{id}")     # match mọi thứ
@app.get("/users/me")       # không bao giờ được gọi
```

> FastAPI match route **theo thứ tự khai báo từ trên xuống**.

---

## E — Path Parameters — Tham Số Trong URL

### E.1 Khai báo cơ bản

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"id": user_id}

# FastAPI tự: parse "42" → int, validate
# Truyền "abc" thay int → 422 Unprocessable Entity tự động
```

### E.2 Nhiều path params

```python
@app.get("/shops/{shop_id}/products/{product_id}")
async def get_product(shop_id: int, product_id: int):
    return {"shop": shop_id, "product": product_id}
```

### E.3 Validate với Path()

```python
from fastapi import Path

@app.get("/users/{user_id}")
async def get_user(
    user_id: int = Path(gt=0, description="ID của user, phải > 0"),
):
    return {"id": user_id}

# user_id=0 hoặc âm → 422 tự động
# description → hiển thị trong /docs
```

### E.4 Path param kiểu Enum — giới hạn giá trị

```python
from enum import Enum

class Status(str, Enum):
    active   = "active"
    inactive = "inactive"
    pending  = "pending"

@app.get("/users/{status}")
async def get_by_status(status: Status):
    return {"status": status}

# /users/active   → OK
# /users/deleted  → 422 (không phải enum value)
# Swagger UI hiển thị dropdown tự động
```

### E.5 Path param nhận cả đường dẫn (/a/b/c)

```python
@app.get("/files/{file_path:path}")
async def get_file(file_path: str):
    return {"path": file_path}

# GET /files/data/2024/report.csv → file_path = "data/2024/report.csv"
```

### E.6 ⚠️ Java vs FastAPI

```java
// Java Spring
@GetMapping("/users/{id}")
public User getUser(@PathVariable @Min(1) Long id) { ... }
```

```python
# FastAPI
@app.get("/users/{id}")
async def get_user(id: int = Path(gt=0)): ...
# Gọn hơn — validation nằm ngay trong khai báo param
```

---

## F — Query Parameters — Tham Số Trên URL ?key=value

### F.1 Khai báo cơ bản

```python
@app.get("/users")
async def list_users(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# GET /users           → skip=0, limit=10 (default)
# GET /users?skip=5    → skip=5, limit=10
# GET /users?limit=abc → 422 (không phải int)
```

> **Quy tắc FastAPI:** param **không có trong `{}`** của path → tự động là **query param**.

### F.2 Required vs Optional query param

```python
# Required — không có default → bắt buộc phải truyền
@app.get("/search")
async def search(q: str):
    return {"query": q}
# GET /search        → 422 (thiếu q)
# GET /search?q=abc  → OK

# Optional — có thể None
async def search(q: str | None = None):
    if q is None:
        return {"results": "tất cả"}
    return {"results": f"tìm: {q}"}
```

### F.3 Validate với Query()

```python
from fastapi import Query

@app.get("/products")
async def list_products(
    skip:   int       = Query(default=0,    ge=0),
    limit:  int       = Query(default=10,   ge=1, le=100),
    search: str | None = Query(default=None, min_length=1, max_length=50),
    sort:   str       = Query(default="id", pattern="^(id|name|price)$"),
):
    return {"skip": skip, "limit": limit, "search": search, "sort": sort}

# ?limit=200  → 422 (vượt le=100)
# ?search=    → 422 (vi phạm min_length=1)
# ?sort=date  → 422 (không match pattern)
```

### F.4 Query param là list

```python
# GET /items?tag=python&tag=fastapi&tag=async
@app.get("/items")
async def get_items(tag: list[str] = Query(default=[])):
    return {"tags": tag}
# → {"tags": ["python", "fastapi", "async"]}
```

### F.5 Alias — tên khác trên URL

```python
# URL dùng dấu - nhưng Python không cho phép - trong tên biến
@app.get("/items")
async def get_items(item_query: str = Query(alias="item-query")):
    return {"q": item_query}
# GET /items?item-query=foo → item_query = "foo"
```

### F.6 ⚠️ Java vs FastAPI

```java
// Java Spring
@GetMapping("/users")
public List<User> list(
    @RequestParam(defaultValue="0") int skip,
    @RequestParam(required=false) String q
) { ... }
```

```python
# FastAPI
@app.get("/users")
async def list_users(skip: int = 0, q: str | None = None): ...
# Không có annotation thêm — type hint IS the config
```

---

## G — Request Body — Nhận JSON Data

### G.1 Khai báo cơ bản

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    age: int | None = None

@app.post("/users")
async def create_user(user: UserCreate):
    # user đã được validate — dùng ngay
    return {"id": 1, **user.model_dump()}

# Body sai schema → 422 tự động với message rõ ràng
```

> **Quy tắc FastAPI:** param có kiểu là **Pydantic BaseModel** → tự động là **request body**.

### G.2 Truy cập dữ liệu trong body

```python
async def create_user(user: UserCreate):
    user.name                   # trực tiếp attribute
    user.email
    user.model_dump()           # → {"name": "Alice", "email": "...", "age": null}
    {"id": 1, **user.model_dump()}  # unpack vào dict mới
```

### G.3 PATCH — Partial update (chỉ update field được gửi)

```python
class UserUpdate(BaseModel):
    name:  str | None = None    # tất cả đều Optional
    email: str | None = None
    age:   int | None = None

@app.patch("/users/{id}")
async def partial_update(id: int, user: UserUpdate):
    # exclude_unset=True → chỉ lấy field client thực sự gửi lên
    update_data = user.model_dump(exclude_unset=True)
    # Gửi {"name": "Bob"} → update_data = {"name": "Bob"} (không có email, age)
    # → không ghi đè field client không gửi
    return update_data
```

### G.4 Nhiều body params với Body()

```python
from fastapi import Body

@app.put("/users/{id}")
async def update_with_note(
    id:         int,
    user:       UserUpdate,
    importance: int = Body(gt=0, description="Mức độ ưu tiên"),
):
    ...
# JSON body cần: {"user": {...}, "importance": 5}
```

### G.5 ⚠️ Java vs FastAPI

```java
// Java Spring
@PostMapping("/users")
public ResponseEntity<User> create(@RequestBody @Valid UserCreateDTO dto) { ... }
// Cần: @RequestBody + @Valid + BindingResult để bắt lỗi
```

```python
# FastAPI
@app.post("/users")
async def create(user: UserCreate): ...
# @RequestBody + @Valid + error handling = tự động
```

---

## H — Kết Hợp Path + Query + Body

### H.1 Quy tắc FastAPI tự phân biệt

| Điều kiện | Loại param |
|-----------|-----------|
| Tên có trong `{...}` của path | **Path param** |
| Kiểu là Pydantic `BaseModel` | **Request body** |
| Có default value hoặc `None` | **Query param** (tùy chọn) |
| Không có default, không trong path, không là Model | **Query param** (bắt buộc) |

### H.2 Ví dụ kết hợp đầy đủ

```python
class ItemUpdate(BaseModel):
    name: str
    price: float

@app.put("/shops/{shop_id}/items/{item_id}")
async def update_item(
    shop_id:  int,              # ← PATH param   (có trong URL)
    item_id:  int,              # ← PATH param   (có trong URL)
    item:     ItemUpdate,       # ← REQUEST BODY (là Pydantic Model)
    notify:   bool  = False,    # ← QUERY param  (có default)
    comment:  str | None = None, # ← QUERY param (Optional)
):
    return {
        "shop": shop_id, "item": item_id,
        "data": item.model_dump(),
        "notify": notify, "comment": comment,
    }

# PUT /shops/1/items/42?notify=true&comment=urgent
# Body: {"name": "Laptop", "price": 25000000}
```

---

## I — Response Model — Kiểm Soát Dữ Liệu Trả Về

### I.1 WHAT & WHY

`response_model` khai báo **schema của response** — FastAPI tự:
- Serialize object → JSON
- **Filter bỏ field thừa** (password, internal fields)
- Validate output trước khi trả về
- Sinh schema cho /docs

### I.2 Khai báo và dùng response_model

```python
class UserCreate(BaseModel):
    name: str
    email: str
    password: str           # ← có password (input)

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    # ← KHÔNG có password → FastAPI tự loại bỏ khi trả về

@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    # Lưu DB... giả sử trả về object có password
    return {
        "id": 1,
        "name": user.name,
        "email": user.email,
        "password": user.password,  # FastAPI tự filter → không có trong response
    }
```

### I.3 response_model cho list

```python
@app.get("/users", response_model=list[UserResponse])
async def list_users():
    return [
        {"id": 1, "name": "Alice", "email": "a@a.com", "password": "secret"},
        {"id": 2, "name": "Bob",   "email": "b@b.com", "password": "secret"},
    ]
# Response: [{"id":1,"name":"Alice","email":"a@a.com"}, ...]
# password bị filter tự động
```

### I.4 Pattern kế thừa schema — chuẩn production

```python
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):         # Input: + password
    password: str

class UserUpdate(BaseModel):        # PATCH: tất cả Optional
    name:  str | None = None
    email: str | None = None

class UserInDB(UserBase):           # DB layer: + id, hashed_password
    id: int
    hashed_password: str

class UserResponse(UserBase):       # Output: + id, KHÔNG có password
    id: int
    model_config = ConfigDict(from_attributes=True)  # đọc từ ORM object
```

> `from_attributes=True` → **bắt buộc** khi dùng SQLAlchemy ORM. FastAPI đọc attribute từ ORM object thay vì dict.

### I.5 ⚠️ Java vs FastAPI

```java
// Java: dùng @JsonIgnore hoặc DTO riêng + ModelMapper
@JsonIgnore
private String password;
// Hoặc: modelMapper.map(user, UserResponseDTO.class)
```

```python
# FastAPI: response_model=UserResponse → tự filter, không cần annotation
@app.post("/users", response_model=UserResponse)
```

---

## J — HTTP Status Codes — Trả Mã Lỗi Chuẩn

### J.1 Các mã quan trọng cần nhớ

| Code | Ý nghĩa | Dùng khi |
|------|---------|----------|
| `200 OK` | Thành công | GET, PUT, PATCH (mặc định) |
| `201 Created` | Tạo mới thành công | POST |
| `204 No Content` | Thành công, không có body | DELETE |
| `400 Bad Request` | Client sai logic nghiệp vụ | Email không đúng format logic |
| `401 Unauthorized` | Chưa xác thực | Thiếu/sai token |
| `403 Forbidden` | Không có quyền | Đúng token nhưng không đủ role |
| `404 Not Found` | Resource không tồn tại | User ID không có trong DB |
| `409 Conflict` | Trùng data | Email đã tồn tại |
| `422 Unprocessable` | Pydantic validation fail | **FastAPI tự trả, không cần xử lý** |
| `500 Internal Error` | Lỗi server | Unhandled exception |

### J.2 Đặt status code

```python
from fastapi import status

@app.post("/users", status_code=201)
async def create_user(user: UserCreate): ...

@app.delete("/users/{id}", status_code=204)
async def delete_user(id: int): ...

# Dùng constant thay số magic — dễ đọc hơn
@app.post("/users", status_code=status.HTTP_201_CREATED)
@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
```

### J.3 HTTPException — Ném lỗi có cấu trúc

```python
from fastapi import HTTPException

@app.get("/users/{id}")
async def get_user(id: int):
    user = fake_db.get(id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User không tồn tại",
        )
    return user
# Response: 404 + {"detail": "User không tồn tại"}

# 401 với header (chuẩn OAuth2)
raise HTTPException(
    status_code=401,
    detail="Token không hợp lệ",
    headers={"WWW-Authenticate": "Bearer"},
)

# detail có thể là bất kỳ JSON value
raise HTTPException(
    status_code=400,
    detail={"code": "EMAIL_TAKEN", "field": "email", "message": "Email đã tồn tại"},
)
```

### J.4 Custom Exception Handler — Xử lý lỗi toàn cục

```python
from fastapi import Request
from fastapi.responses import JSONResponse

# 1. Định nghĩa exception
class BusinessError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

# 2. Đăng ký handler
@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message},
    )

# 3. Ném từ bất kỳ endpoint
@app.post("/users")
async def create_user(user: UserCreate):
    if email_exists(user.email):
        raise BusinessError("EMAIL_TAKEN", "Email đã tồn tại", 409)
    ...
```

### J.5 ⚠️ Java vs FastAPI

| Spring Boot | FastAPI |
|-------------|---------|
| `@ResponseStatus(HttpStatus.NOT_FOUND)` | `status_code=404` trong decorator |
| `throw new ResponseStatusException(HttpStatus.NOT_FOUND, "msg")` | `raise HTTPException(status_code=404, detail="msg")` |
| `@ControllerAdvice` + `@ExceptionHandler` | `@app.exception_handler(ExceptionClass)` |
| `MethodArgumentNotValidException` → 400 | `ValidationError` → **422 tự động** |

---

## K — Java vs FastAPI — Bảng Đối Chiếu Khối 9

| Khái niệm | Spring Boot | FastAPI |
|-----------|-------------|---------|
| Khởi tạo app | `@SpringBootApplication` + `main()` | `app = FastAPI()` + `uvicorn` |
| Định nghĩa endpoint | `@GetMapping` trong `@RestController` class | `@app.get` trên function |
| Path param | `@PathVariable Long id` | `id: int` (tên trùng `{id}`) |
| Query param | `@RequestParam(defaultValue="0") int skip` | `skip: int = 0` |
| Request body | `@RequestBody @Valid UserDTO dto` | `user: UserCreate` |
| Response schema | `@JsonIgnore`, ModelMapper, `@JsonView` | `response_model=UserResponse` |
| Ném lỗi | `throw new ResponseStatusException(...)` | `raise HTTPException(...)` |
| Global exception | `@ControllerAdvice` + `@ExceptionHandler` | `@app.exception_handler(...)` |
| API Documentation | Springfox/Springdoc dependency + config | `/docs` `/redoc` tự động |
| Validation fail | `MethodArgumentNotValidException` → 400 | `ValidationError` → **422 tự động** |

---

## L — Bài Tập Thực Hành

```python
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
```

---

## Tóm Tắt — Điểm Cần Nhớ

| Điều | Ghi nhớ |
|------|---------|
| Path param | Tên trùng `{...}` trong decorator + type hint là đủ |
| Query param | Param bình thường có default hoặc `None` |
| Request body | Param kiểu Pydantic `BaseModel` |
| FastAPI phân biệt tự động | Không cần annotation `@PathVariable`, `@RequestParam`, `@RequestBody` |
| 422 | Pydantic fail → FastAPI tự trả, không cần code |
| response_model | Filter password, control output schema |
| Thứ tự route | Specific trước, generic (`{id}`) sau |
| async def | Khi có `await` (DB/HTTP) | `def` khi không có I/O |
