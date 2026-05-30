# 10 — Request & Response Nâng Cao

> **Khối 10 — Request & Response Nâng Cao**
> Dành cho Java developer — tập trung vào điểm khác biệt so với Spring Boot.

---

## A — Form Data & File Upload

### A.1 WHAT — Form Data là gì?

- Dữ liệu gửi qua `Content-Type: application/x-www-form-urlencoded` hoặc `multipart/form-data`
- Dùng khi HTML `<form>` submit hoặc upload file — **không phải JSON**
- FastAPI dùng `Form()` và `UploadFile` từ `fastapi`
- Cần cài thêm: `python-multipart` (FastAPI sẽ báo lỗi nếu thiếu)

```bash
uv add python-multipart
# hoặc
pip install python-multipart
```

### A.2 Form Data — Đọc field từ form

```python
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login")
async def login(
    username: str = Form(...),          # bắt buộc
    password: str = Form(...),
    remember: bool = Form(default=False),
):
    return {"username": username, "remember": remember}

# Content-Type: application/x-www-form-urlencoded
# Body: username=alice&password=secret&remember=true
```

> ⚠️ **Không thể mix Form + JSON Body** trong cùng 1 endpoint.
> Form dùng `Content-Type: multipart` hoặc `urlencoded`, JSON dùng `application/json` — khác nhau hoàn toàn.

### A.3 File Upload — Nhận file đơn

```python
from fastapi import FastAPI, UploadFile, File

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()         # đọc toàn bộ nội dung (bytes)
    return {
        "filename":     file.filename,
        "content_type": file.content_type,
        "size":         len(content),
    }

# Content-Type: multipart/form-data
# form-data key: file, value: <binary file>
```

### A.4 File Upload — Nhiều file + kết hợp Form field

```python
from typing import Annotated

@app.post("/upload/multiple")
async def upload_multiple(
    description: str       = Form(...),
    files:       list[UploadFile] = File(...),
):
    results = []
    for f in files:
        content = await f.read()
        results.append({"name": f.filename, "size": len(content)})
    return {"description": description, "files": results}
```

### A.5 Lưu file lên disk

```python
import shutil
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload/save")
async def save_file(file: UploadFile = File(...)):
    dest = UPLOAD_DIR / file.filename
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)   # stream copy — không load hết vào RAM
    return {"saved_to": str(dest)}
```

> ✅ Dùng `shutil.copyfileobj` thay vì `await file.read()` để tránh load file lớn vào RAM.

### A.6 Validate file — type & size

```python
from fastapi import HTTPException

MAX_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}

@app.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, detail=f"Chỉ nhận: {ALLOWED_TYPES}")

    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(413, detail="File quá lớn, tối đa 5MB")

    return {"filename": file.filename, "size": len(content)}
```

### A.7 ⚠️ Java vs FastAPI

| Spring Boot | FastAPI |
|-------------|---------|
| `@RequestParam MultipartFile file` | `file: UploadFile = File(...)` |
| `@RequestParam String field` trong multipart | `field: str = Form(...)` |
| `file.getBytes()` | `await file.read()` |
| `file.transferTo(dest)` | `shutil.copyfileobj(file.file, buffer)` |

---

## B — Request Headers & Cookies

### B.1 Đọc Header

```python
from fastapi import Header

@app.get("/info")
async def get_info(
    user_agent:    str | None = Header(default=None),
    accept_language: str | None = Header(default=None),
    x_request_id:  str | None = Header(default=None),
):
    return {
        "user_agent":    user_agent,
        "language":      accept_language,
        "request_id":    x_request_id,
    }

# FastAPI tự convert: x_request_id → "X-Request-Id" (dấu _ → -)
```

> **Quy tắc:** FastAPI tự chuyển `_` thành `-` khi map tên biến → tên header HTTP.
> `user_agent` → header `User-Agent` | `x_request_id` → header `X-Request-Id`

### B.2 Custom Header — API Key auth đơn giản

```python
from fastapi import Header, HTTPException

API_KEY = "secret-key-123"

@app.get("/secure")
async def secure_endpoint(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="API Key không hợp lệ")
    return {"data": "Dữ liệu bảo mật"}

# Header: X-Api-Key: secret-key-123
```

### B.3 Đọc Cookie

```python
from fastapi import Cookie

@app.get("/profile")
async def get_profile(
    session_id: str | None = Cookie(default=None),
    theme:      str        = Cookie(default="light"),
):
    if session_id is None:
        raise HTTPException(status_code=401, detail="Chưa đăng nhập")
    return {"session": session_id, "theme": theme}
```

### B.4 Set Cookie trong Response

```python
from fastapi import Response
from fastapi.responses import JSONResponse

@app.post("/login")
async def login(response: Response, username: str = Form(...)):
    # Set cookie vào response object được inject
    response.set_cookie(
        key="session_id",
        value="token-abc-123",
        httponly=True,          # JS không đọc được → bảo mật hơn
        samesite="lax",
        max_age=3600,           # seconds
        # secure=True,          # bật khi HTTPS
    )
    return {"message": f"Xin chào {username}"}

@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie("session_id")
    return {"message": "Đã đăng xuất"}
```

### B.5 ⚠️ Java vs FastAPI

| Spring Boot | FastAPI |
|-------------|---------|
| `@RequestHeader("User-Agent") String ua` | `user_agent: str = Header(...)` |
| `@CookieValue("session") String s` | `session: str = Cookie(...)` |
| `response.addCookie(new Cookie(...))` | `response.set_cookie(...)` |

---

## C — HTTPException — Lỗi Có Cấu Trúc

### C.1 WHAT — HTTPException là gì?

- Class built-in của FastAPI để trả HTTP error response có cấu trúc
- FastAPI tự serialize thành `{"detail": "..."}` với đúng HTTP status code
- Dùng `raise` thay vì `return` — giống throw exception trong Java

### C.2 Cách dùng cơ bản

```python
from fastapi import FastAPI, HTTPException

@app.get("/users/{id}")
async def get_user(id: int):
    user = db.get(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    return user

# Response:
# HTTP 404
# {"detail": "User không tồn tại"}
```

### C.3 detail có thể là bất kỳ JSON value

```python
# String
raise HTTPException(404, detail="Not found")

# Dict — structured error
raise HTTPException(400, detail={
    "code":    "EMAIL_TAKEN",
    "field":   "email",
    "message": "Email đã được đăng ký",
})

# List — nhiều lỗi
raise HTTPException(422, detail=[
    {"field": "email",    "error": "Không hợp lệ"},
    {"field": "password", "error": "Quá ngắn"},
])
```

### C.4 Thêm Response Headers vào lỗi

```python
# Chuẩn OAuth2: 401 phải kèm WWW-Authenticate header
raise HTTPException(
    status_code=401,
    detail="Token hết hạn",
    headers={"WWW-Authenticate": "Bearer"},
)
```

### C.5 ⚠️ Java vs FastAPI

```java
// Java Spring
throw new ResponseStatusException(HttpStatus.NOT_FOUND, "User không tồn tại");
```

```python
# FastAPI
raise HTTPException(status_code=404, detail="User không tồn tại")
```

---

## D — Custom Exception Handler — Xử Lý Lỗi Toàn Cục

### D.1 WHY — Tại sao cần Custom Exception Handler?

- `HTTPException` trả `{"detail": "..."}` — đủ dùng cho lỗi đơn giản
- Production cần format lỗi **nhất quán toàn hệ thống**: code, message, field...
- Xử lý lỗi **một lần** ở tầng global thay vì mỗi endpoint tự catch
- Tương đương `@ControllerAdvice` trong Spring Boot

### D.2 Override handler của HTTPException

```python
from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code":    exc.status_code,
                "message": exc.detail,
                "path":    str(request.url),
            },
        },
        headers=exc.headers,
    )

# Mọi HTTPException trong app đều trả format trên
```

### D.3 Custom Business Exception

```python
# exceptions.py

class AppException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code        = code
        self.message     = message
        self.status_code = status_code

class NotFoundException(AppException):
    def __init__(self, resource: str, id: int | str):
        super().__init__(
            code=       "NOT_FOUND",
            message=    f"{resource} với id={id} không tồn tại",
            status_code=404,
        )

class DuplicateException(AppException):
    def __init__(self, field: str, value: str):
        super().__init__(
            code=       "DUPLICATE",
            message=    f"Giá trị '{value}' đã tồn tại tại field '{field}'",
            status_code=409,
        )
```

```python
# main.py — đăng ký handler

from fastapi.exceptions import RequestValidationError

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "code": exc.code, "message": exc.message},
    )

# Override cả 422 Validation Error của Pydantic
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {"field": ".".join(str(x) for x in e["loc"]), "message": e["msg"]}
        for e in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"success": False, "code": "VALIDATION_ERROR", "errors": errors},
    )
```

```python
# Dùng trong endpoint
@app.get("/users/{id}")
async def get_user(id: int):
    user = db.get(id)
    if user is None:
        raise NotFoundException("User", id)     # ← gọn hơn HTTPException
    return user

@app.post("/users")
async def create_user(user: UserCreate):
    if email_exists(user.email):
        raise DuplicateException("email", user.email)
    ...
```

### D.4 ⚠️ Java vs FastAPI

| Spring Boot | FastAPI |
|-------------|---------|
| `@ControllerAdvice` class | `@app.exception_handler(ExcClass)` function |
| `@ExceptionHandler(MyException.class)` | Argument type của handler function |
| `ResponseEntityExceptionHandler` | `@app.exception_handler(RequestValidationError)` |
| `ProblemDetail` (RFC 9457) | Tự định nghĩa format trong `JSONResponse` |

---

## E — Direct Response — JSONResponse, HTMLResponse, FileResponse

### E.1 WHAT — Khi nào cần Direct Response?

- Mặc định FastAPI tự serialize return value → JSON
- **Direct Response** khi cần kiểm soát hoàn toàn: headers, cookies, content-type, streaming
- Các loại: `JSONResponse`, `HTMLResponse`, `PlainTextResponse`, `FileResponse`, `StreamingResponse`, `RedirectResponse`

### E.2 JSONResponse — Kiểm soát headers và status

```python
from fastapi.responses import JSONResponse

@app.get("/data")
async def get_data():
    return JSONResponse(
        status_code=200,
        content={"key": "value"},
        headers={
            "X-Custom-Header": "hello",
            "Cache-Control":   "max-age=300",
        },
    )
```

> ⚠️ Khi dùng `JSONResponse` trực tiếp, `response_model` **không có tác dụng** — FastAPI bỏ qua bước serialize/filter.

### E.3 HTMLResponse — Trả HTML

```python
from fastapi.responses import HTMLResponse

@app.get("/page", response_class=HTMLResponse)
async def get_page():
    html = """
    <html><body>
        <h1>Hello FastAPI</h1>
        <p>Đây là HTML response.</p>
    </body></html>
    """
    return HTMLResponse(content=html, status_code=200)
```

### E.4 FileResponse — Tải file về

```python
from fastapi.responses import FileResponse
from pathlib import Path

@app.get("/download/{filename}")
async def download_file(filename: str):
    path = Path("uploads") / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="File không tồn tại")

    return FileResponse(
        path=str(path),
        filename=filename,               # tên file khi người dùng tải về
        media_type="application/octet-stream",
    )
```

### E.5 StreamingResponse — Trả dữ liệu lớn theo luồng

```python
from fastapi.responses import StreamingResponse
import io

@app.get("/stream/csv")
async def stream_csv():
    def generate():
        yield "id,name,price\n"
        for i in range(1, 10001):
            yield f"{i},Product {i},{i * 1000}\n"

    return StreamingResponse(
        generate(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=products.csv"},
    )
```

### E.6 RedirectResponse

```python
from fastapi.responses import RedirectResponse

@app.get("/old-path")
async def redirect():
    return RedirectResponse(url="/new-path", status_code=301)
```

### E.7 ⚠️ Java vs FastAPI

| Spring Boot | FastAPI |
|-------------|---------|
| `ResponseEntity<String>` với headers | `JSONResponse(content=..., headers=...)` |
| `@ResponseBody` + `MediaType.TEXT_HTML_VALUE` | `HTMLResponse(content=...)` |
| `Resource` return type + `InputStreamResource` | `FileResponse(path=...)` |
| `StreamingResponseBody` | `StreamingResponse(generator)` |

---

## F — Background Tasks — Tác Vụ Nền

### F.1 WHAT & WHY

- Thực hiện tác vụ **sau khi** đã trả response về client
- Client nhận response nhanh, server tiếp tục xử lý ở background
- Dùng cho: gửi email xác nhận, ghi log, resize ảnh, push notification...
- **Không dùng** cho tác vụ nặng (AI, video processing) → dùng Celery/ARQ

### F.2 Cách dùng cơ bản

```python
from fastapi import BackgroundTasks

def send_welcome_email(email: str, username: str):
    # Hàm sync thường — FastAPI chạy trong thread pool
    print(f"[EMAIL] Gửi email chào mừng đến {email} cho {username}")
    # Thực tế: gọi SMTP, SendGrid, SES...

@app.post("/users", status_code=201)
async def create_user(
    user:             UserCreate,
    background_tasks: BackgroundTasks,
):
    # Tạo user trong DB...
    new_user = {"id": 1, **user.model_dump()}

    # Đăng ký task — chạy SAU khi response được gửi
    background_tasks.add_task(send_welcome_email, user.email, user.name)

    return new_user  # ← Client nhận response ngay, không chờ email
```

### F.3 Async background task

```python
async def log_request(user_id: int, action: str):
    # Hàm async — chạy trong event loop, không block
    await audit_db.insert({"user_id": user_id, "action": action})

@app.delete("/users/{id}", status_code=204)
async def delete_user(id: int, background_tasks: BackgroundTasks):
    if id not in db:
        raise HTTPException(404, "Không tìm thấy")
    del db[id]
    background_tasks.add_task(log_request, id, "DELETE_USER")
    # Không return gì → 204 No Content
```

### F.4 Nhiều tasks

```python
@app.post("/orders")
async def create_order(order: OrderCreate, background_tasks: BackgroundTasks):
    new_order = save_order(order)

    background_tasks.add_task(send_order_confirmation, order.email, new_order.id)
    background_tasks.add_task(update_inventory,         order.items)
    background_tasks.add_task(notify_warehouse,         new_order.id)

    return new_order  # 3 tasks chạy lần lượt sau khi trả response
```

### F.5 ⚠️ Java vs FastAPI

| Spring Boot | FastAPI |
|-------------|---------|
| `@Async` + `CompletableFuture` | `BackgroundTasks.add_task(func, ...)` |
| `ThreadPoolTaskExecutor` | FastAPI tự quản lý thread pool |
| `@EventListener(ApplicationReadyEvent)` | Không tương đương — đây là startup event |

---

## G — APIRouter — Tách Route Theo Module

### G.1 WHY — Tại sao cần APIRouter?

- `main.py` một file với 50+ endpoint → khó quản lý
- `APIRouter` = **Blueprint (Flask)** = **@Controller (Spring Boot)** nhưng là function-based
- Tách theo domain: `users`, `products`, `orders`... mỗi cái 1 file riêng

### G.2 Khai báo Router

```python
# routers/users.py

from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/users",          # /users/... tự động thêm vào mọi route
    tags=["Users"],           # nhóm trong /docs
    responses={404: {"description": "User không tìm thấy"}},
)

@router.get("/")              # thực tế là GET /users/
async def list_users():
    return [{"id": 1, "name": "Alice"}]

@router.get("/{id}")          # thực tế là GET /users/{id}
async def get_user(id: int):
    return {"id": id}

@router.post("/", status_code=201)
async def create_user(user: UserCreate):
    return {"id": 99, **user.model_dump()}
```

### G.3 Đăng ký Router vào app

```python
# main.py

from fastapi import FastAPI
from routers import users, products, orders

app = FastAPI(title="My API", version="1.0.0")

app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router,  prefix="/v1")   # override prefix
```

### G.4 Router Dependencies — Áp dụng cho cả router

```python
from fastapi import Depends

async def verify_token(x_api_key: str = Header(...)):
    if x_api_key != "secret":
        raise HTTPException(403, "Unauthorized")

# Mọi endpoint trong router này đều yêu cầu token
router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(verify_token)],   # ← global dep cho router
)
```

### G.5 ⚠️ Java vs FastAPI

| Spring Boot | FastAPI |
|-------------|---------|
| `@RestController @RequestMapping("/users")` class | `router = APIRouter(prefix="/users")` |
| `@GetMapping("/{id}")` trong controller | `@router.get("/{id}")` |
| `@ComponentScan` auto-detect | `app.include_router(router)` explicit |

---

## H — Cấu Trúc Thư Mục Dự Án FastAPI Chuẩn

### H.1 Cấu trúc khuyến nghị

```
my-api/
├── main.py                     ← entry point, khởi tạo app, include routers
├── pyproject.toml              ← dependencies (uv)
├── .env                        ← biến môi trường (không commit)
├── .env.example                ← mẫu biến môi trường (commit)
│
├── app/
│   ├── __init__.py
│   │
│   ├── core/
│   │   ├── config.py           ← Pydantic Settings đọc .env
│   │   └── exceptions.py       ← AppException, NotFoundException...
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py            ← APIRouter cho /users
│   │   ├── products.py         ← APIRouter cho /products
│   │   └── orders.py
│   │
│   ├── schemas/
│   │   ├── user.py             ← UserCreate, UserResponse, UserUpdate
│   │   └── product.py
│   │
│   ├── models/                 ← SQLAlchemy ORM models (Khối 11)
│   │   └── user.py
│   │
│   └── services/               ← Business logic (không để trong router)
│       └── user_service.py
│
└── tests/
    ├── conftest.py
    └── test_users.py
```

### H.2 main.py chuẩn

```python
# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.exceptions import AppException, app_exception_handler
from app.routers import users, products

app = FastAPI(
    title=    settings.APP_NAME,
    version=  settings.APP_VERSION,
    docs_url= "/docs" if settings.ENV != "production" else None,
    redoc_url="/redoc" if settings.ENV != "production" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=    settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=    ["*"],
    allow_headers=    ["*"],
)

app.add_exception_handler(AppException, app_exception_handler)

app.include_router(users.router)
app.include_router(products.router)

@app.get("/health", tags=["System"])
async def health():
    return {"status": "ok", "version": settings.APP_VERSION}
```

### H.3 config.py — Pydantic Settings

```python
# app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME:     str  = "My API"
    APP_VERSION:  str  = "1.0.0"
    ENV:          str  = "development"
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()
```

---

## I — CORS Middleware — Cho Phép Frontend Gọi API

### I.1 WHAT — CORS là gì?

- **Cross-Origin Resource Sharing** — cơ chế trình duyệt bảo vệ
- Browser chặn request từ `localhost:3000` (React) đến `localhost:8000` (FastAPI) nếu không cấu hình CORS
- Server phải trả header `Access-Control-Allow-Origin` cho phép

### I.2 Cấu hình cơ bản

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",          # React dev
        "http://localhost:5173",          # Vite dev
        "https://myapp.vercel.app",       # Production frontend
    ],
    allow_credentials=True,              # cho phép gửi cookie
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],                 # cho phép mọi header
)
```

### I.3 Allow all origins (dev only)

```python
# ⚠️ CHỈ dùng trong development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Tất cả origin
    allow_methods=["*"],
    allow_headers=["*"],
)
# ❌ KHÔNG dùng allow_origins=["*"] + allow_credentials=True cùng nhau → lỗi
```

### I.4 Pattern theo môi trường

```python
import os

CORS_ORIGINS = (
    ["*"]
    if os.getenv("ENV") == "development"
    else [
        "https://app.example.com",
        "https://admin.example.com",
    ]
)

app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, ...)
```

---

## J — Middleware Tự Xây Dựng — Logging & Request Timing

### J.1 WHAT — Middleware là gì?

- Code chạy **trước và sau** mỗi request — giống `Filter` trong Java Servlet
- Dùng cho: logging, timing, auth check, rate limit, request ID...
- FastAPI dùng Starlette middleware — 2 cách: `@app.middleware("http")` hoặc class `BaseHTTPMiddleware`

### J.2 Cách 1 — Decorator middleware (đơn giản)

```python
import time
import uuid
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    start      = time.time()

    # Trước khi xử lý request
    print(f"[{request_id}] → {request.method} {request.url.path}")

    response = await call_next(request)    # ← gọi endpoint thực sự

    # Sau khi có response
    duration = (time.time() - start) * 1000
    print(f"[{request_id}] ← {response.status_code} ({duration:.1f}ms)")

    # Thêm header vào response
    response.headers["X-Request-Id"]   = request_id
    response.headers["X-Process-Time"] = f"{duration:.1f}ms"

    return response
```

### J.3 Cách 2 — Class Middleware (có state, cấu hình được)

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class TimingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, slow_threshold_ms: float = 500):
        super().__init__(app)
        self.slow_threshold_ms = slow_threshold_ms

    async def dispatch(self, request: Request, call_next):
        start    = time.time()
        response = await call_next(request)
        duration = (time.time() - start) * 1000

        if duration > self.slow_threshold_ms:
            print(f"⚠️ SLOW REQUEST: {request.url.path} - {duration:.0f}ms")

        response.headers["X-Process-Time"] = f"{duration:.1f}ms"
        return response

# Đăng ký
app.add_middleware(TimingMiddleware, slow_threshold_ms=300)
```

### J.4 Thứ tự middleware — QUAN TRỌNG

```python
# Middleware được thực thi theo thứ tự NGƯỢC với add_middleware
# (LIFO — Last In, First Out)

app.add_middleware(CORSMiddleware, ...)     # ← xử lý THỨ 2 khi request vào
app.add_middleware(TimingMiddleware, ...)   # ← xử lý ĐẦU TIÊN khi request vào

# Request: TimingMiddleware → CORSMiddleware → Endpoint
# Response: Endpoint → CORSMiddleware → TimingMiddleware
```

> ✅ **Luôn** add `CORSMiddleware` trước (thứ tự code) để nó được xử lý sau cùng khi request vào — đảm bảo CORS headers luôn có mặt kể cả khi lỗi.

### J.5 ⚠️ Java vs FastAPI

| Spring Boot | FastAPI |
|-------------|---------|
| `OncePerRequestFilter` | `@app.middleware("http")` decorator |
| `Filter` + `FilterChain.doFilter()` | `await call_next(request)` |
| `@Order(1)` để sắp thứ tự | Thứ tự `add_middleware()` (LIFO) |
| `HandlerInterceptor` | Cũng dùng middleware hoặc `Depends()` |

---

## K — Java vs FastAPI — Bảng Đối Chiếu Khối 10

| Khái niệm | Spring Boot | FastAPI |
|-----------|-------------|---------|
| Form upload | `@RequestParam MultipartFile` | `file: UploadFile = File(...)` |
| Read header | `@RequestHeader String ua` | `user_agent: str = Header(...)` |
| Read cookie | `@CookieValue String s` | `session: str = Cookie(...)` |
| Set cookie | `HttpServletResponse.addCookie()` | `response.set_cookie(...)` |
| Throw HTTP error | `throw new ResponseStatusException(...)` | `raise HTTPException(...)` |
| Global error handler | `@ControllerAdvice` | `@app.exception_handler(ExcClass)` |
| HTML/File response | `ResponseEntity` + `MediaType` | `HTMLResponse`, `FileResponse` |
| Async after response | `@Async` | `BackgroundTasks.add_task(...)` |
| Route grouping | `@RestController @RequestMapping` | `APIRouter(prefix=..., tags=...)` |
| CORS | `CorsConfigurationSource` Bean | `CORSMiddleware` |
| Request filter | `OncePerRequestFilter` | `@app.middleware("http")` |

---

## L — Bài Tập Thực Hành

```python
# ============================================================
# Bài 1 — Form Login + Cookie Session
# ============================================================

from fastapi import FastAPI, Form, Cookie, Response, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="Block 10 Practice")

USERS = {"alice": "password123", "bob": "qwerty"}
SESSIONS: dict[str, str] = {}

@app.post("/auth/login", tags=["Auth"])
async def login(
    response:  Response,
    username:  str = Form(...),
    password:  str = Form(...),
):
    if USERS.get(username) != password:
        raise HTTPException(status_code=401, detail="Sai tài khoản hoặc mật khẩu")

    session_id = f"sess-{username}-abc123"
    SESSIONS[session_id] = username
    response.set_cookie("session_id", session_id, httponly=True, max_age=3600)
    return {"message": f"Xin chào {username}"}

@app.get("/auth/me", tags=["Auth"])
async def me(session_id: str | None = Cookie(default=None)):
    if not session_id or session_id not in SESSIONS:
        raise HTTPException(401, "Chưa đăng nhập")
    return {"username": SESSIONS[session_id]}

@app.post("/auth/logout", tags=["Auth"])
async def logout(response: Response):
    response.delete_cookie("session_id")
    return {"message": "Đã đăng xuất"}


# ============================================================
# Bài 2 — File Upload với Validation
# ============================================================

import shutil
from pathlib import Path
from fastapi import UploadFile, File

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

MAX_SIZE      = 2 * 1024 * 1024   # 2 MB
ALLOWED_TYPES = {"image/jpeg", "image/png"}

@app.post("/files/upload", tags=["Files"])
async def upload(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, f"Chỉ nhận JPEG/PNG, nhận được: {file.content_type}")

    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(413, "File quá lớn, tối đa 2MB")

    dest = UPLOAD_DIR / file.filename
    dest.write_bytes(content)
    return {"filename": file.filename, "size": len(content)}

from fastapi.responses import FileResponse

@app.get("/files/{filename}", tags=["Files"])
async def download(filename: str):
    path = UPLOAD_DIR / filename
    if not path.exists():
        raise HTTPException(404, "File không tìm thấy")
    return FileResponse(path, filename=filename)


# ============================================================
# Bài 3 — Custom Exception + Handler toàn cục
# ============================================================

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

class AppError(Exception):
    def __init__(self, code: str, message: str, status: int = 400):
        self.code, self.message, self.status = code, message, status

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(exc.status, {"success": False, "code": exc.code, "message": exc.message})

@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    errors = [{"field": ".".join(str(x) for x in e["loc"][1:]), "message": e["msg"]}
              for e in exc.errors()]
    return JSONResponse(422, {"success": False, "code": "VALIDATION_ERROR", "errors": errors})

from pydantic import BaseModel, Field

class OrderCreate(BaseModel):
    product_id: int   = Field(gt=0)
    quantity:   int   = Field(ge=1, le=100)
    note:       str | None = None

PRODUCTS = {1: {"name": "Laptop", "stock": 5}, 2: {"name": "Mouse", "stock": 0}}

@app.post("/orders", status_code=201, tags=["Orders"])
async def create_order(order: OrderCreate):
    product = PRODUCTS.get(order.product_id)
    if not product:
        raise AppError("NOT_FOUND", f"Sản phẩm {order.product_id} không tồn tại", 404)
    if product["stock"] < order.quantity:
        raise AppError("OUT_OF_STOCK", f"Chỉ còn {product['stock']} sản phẩm", 409)
    return {"status": "created", "product": product["name"], "qty": order.quantity}


# ============================================================
# Bài 4 — Background Tasks
# ============================================================

from fastapi import BackgroundTasks
import time

def send_email(to: str, subject: str, body: str):
    time.sleep(2)   # Giả lập gửi email mất 2 giây
    print(f"[EMAIL SENT] to={to} subject={subject}")

@app.post("/orders/{order_id}/confirm", tags=["Orders"])
async def confirm_order(
    order_id:         int,
    email:            str,
    background_tasks: BackgroundTasks,
):
    # Trả response ngay — client không chờ email
    background_tasks.add_task(
        send_email,
        to=      email,
        subject= f"Xác nhận đơn hàng #{order_id}",
        body=    f"Đơn hàng #{order_id} đã được xác nhận.",
    )
    return {"order_id": order_id, "status": "confirmed", "note": "Email đang được gửi"}


# ============================================================
# Bài 5 — APIRouter + Middleware tổng hợp
# ============================================================

import time, uuid
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware

# --- Middleware: timing + request id ---
@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    rid   = str(uuid.uuid4())[:8]
    start = time.time()
    resp  = await call_next(request)
    ms    = (time.time() - start) * 1000
    resp.headers["X-Request-Id"]   = rid
    resp.headers["X-Process-Time"] = f"{ms:.1f}ms"
    if ms > 200:
        print(f"⚠️ SLOW [{rid}] {request.url.path} {ms:.0f}ms")
    return resp

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Router tách module ---
product_router = APIRouter(prefix="/products", tags=["Products"])
PROD_DB: dict[int, dict] = {1: {"id": 1, "name": "Laptop"}}

@product_router.get("/")
async def list_products():
    return list(PROD_DB.values())

@product_router.get("/{id}")
async def get_product(id: int):
    if id not in PROD_DB:
        raise AppError("NOT_FOUND", f"Product {id} không tồn tại", 404)
    return PROD_DB[id]

app.include_router(product_router)

# Chạy: uvicorn main:app --reload
# Test: http://localhost:8000/docs
# Xem headers: X-Request-Id, X-Process-Time trong response headers của Swagger
```

---

## Tóm Tắt — Điểm Cần Nhớ

| Điều | Ghi nhớ |
|------|---------|
| Form Data | Cần `python-multipart`, dùng `Form()`, không mix với JSON body |
| File Upload | `UploadFile = File(...)`, dùng `shutil.copyfileobj` để stream lớn |
| Header | `user_agent: str = Header(...)` — dấu `_` tự chuyển thành `-` |
| Cookie | Đọc: `Cookie(...)` | Set: `response.set_cookie(...)` |
| HTTPException | `raise HTTPException(404, detail="...")` — detail có thể là dict/list |
| Custom Handler | `@app.exception_handler(ExcClass)` — xử lý 1 lần toàn global |
| Validation Error | Override `@app.exception_handler(RequestValidationError)` để format 422 |
| JSONResponse trực tiếp | `response_model` **không có tác dụng** khi dùng JSONResponse |
| Background Tasks | Inject `BackgroundTasks` vào endpoint, gọi `add_task(func, *args)` |
| APIRouter | `prefix` + `tags` trong constructor, `app.include_router()` khi đăng ký |
| CORS | `add_middleware(CORSMiddleware, allow_origins=[...])` — bắt buộc cho frontend |
| Middleware thứ tự | LIFO — middleware add sau chạy trước khi request đến |
