# Phase 6 — main.py

## Trạng Thái

- [ ] Đang làm
- [x] Hoàn thành

**Bắt đầu:** 2026-06-02  
**Kết thúc:** 2026-06-02

---

## Tổng Quan Phase Này

**Làm gì:** Viết `app/main.py` — wiring tất cả lại với nhau.

**main.py là "composition root"** — nơi duy nhất biết về tất cả layers:
- Include routers
- Register exception handlers
- Add middleware
- Lifespan (startup/shutdown)

**Kết quả mong đợi:** Server chạy được:
```bash
uv run uvicorn app.main:app --reload
# Mong đợi: Uvicorn running on http://127.0.0.1:8000
```

---

## Các Bước Thực Hiện

### Bước 6.1 — Lifespan

**Làm gì:** Dùng `@asynccontextmanager` để handle startup/shutdown.

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting up {settings.APP_NAME} v{settings.APP_VERSION}...")
    yield
    print("Shutting down...")
```

**Tại sao dùng lifespan thay vì `@app.on_event("startup")`?**
- `on_event` deprecated trong FastAPI >= 0.93
- Lifespan là context manager → startup và shutdown nằm cùng 1 chỗ, dễ đọc
- Cleanup (`yield` trở xuống) luôn chạy ngay cả khi startup có exception

**Kiến thức áp dụng:** Khối 11 — async context manager

---

### Bước 6.2 — CORS Middleware

**Làm gì:** Cho phép frontend (React/Vue) gọi API từ port khác.

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Tại sao cần CORS?**
Frontend chạy trên port 3000 hoặc 5173 → browser block request theo same-origin policy.
CORS middleware thêm `Access-Control-Allow-Origin` header → browser cho phép.

**Kiến thức áp dụng:** Khối 10 — Middleware

---

### Bước 6.3 — Request Logging Middleware

**Làm gì:** Log method, path, status code, duration và gán request ID cho mỗi request.

```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"[{request_id}] {request.method} {request.url.path} -> {response.status_code} ({duration:.3f}s)")
    response.headers["X-Request-Id"] = request_id
    return response
```

**Tại sao thêm `X-Request-Id` header?**
Khi có nhiều requests đồng thời, log dễ bị lẫn.
`X-Request-Id` cho phép trace 1 request end-to-end qua logs.

**Kiến thức áp dụng:** Khối 10 — Custom middleware

---

### Bước 6.4 — Exception Handlers

**Làm gì:** Convert custom exceptions thành JSON response đúng format.

```python
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    error_code = type(exc).__name__.replace("Exception", "").upper()
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_code": error_code, "message": exc.message, "detail": None},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"error_code": "INTERNAL_ERROR", "message": "An unexpected error occurred.", "detail": None},
    )
```

**Tại sao handler cho `AppException` bắt được cả `NotFoundException` và `BusinessException`?**
Cả hai đều kế thừa `AppException` → FastAPI match handler theo MRO (Method Resolution Order).
Không cần đăng ký riêng cho từng subclass.

**Format lỗi đồng nhất:**
```json
{
  "error_code": "NOTFOUND",
  "message": "Category with id=99 not found",
  "detail": null
}
```

**Kiến thức áp dụng:** Khối 10 — Exception handlers

---

### Bước 6.5 — Include Routers

**Làm gì:** Mount tất cả routers dưới prefix `/api/v1`.

```python
API_PREFIX = "/api/v1"

app.include_router(categories_router, prefix=API_PREFIX)
app.include_router(transactions_router, prefix=API_PREFIX)
app.include_router(reports_router, prefix=API_PREFIX)
```

**Kết quả URL pattern:**
- `GET /api/v1/categories/`
- `POST /api/v1/transactions/`
- `GET /api/v1/reports/summary`
- `GET /health` (không có prefix — health check riêng)

---

### Bước 6.6 — Chạy và Verify

```bash
uv run uvicorn app.main:app --reload
```

**Verify thủ công:**
```bash
# Health check
curl http://127.0.0.1:8000/health
# {"status":"ok","version":"1.0.0"}

# Categories (empty DB)
curl http://127.0.0.1:8000/api/v1/categories/
# []

# Report summary (empty DB)
curl http://127.0.0.1:8000/api/v1/reports/summary
# {"total_income":"0","total_expense":"0","balance":"0"}
```

**Swagger UI:** mở `http://127.0.0.1:8000/docs` — xem và test API trực tiếp trên browser.

---

## Kiến Thức Áp Dụng Trong Phase Này

| Kiến thức | Áp dụng cụ thể |
|----------|---------------|
| `@asynccontextmanager` | Lifespan startup/shutdown |
| `CORSMiddleware` | Cross-Origin Resource Sharing |
| `@app.middleware("http")` | Request/response logging + X-Request-Id |
| `app.add_exception_handler()` | Convert custom exceptions → JSON response |
| `app.include_router()` | Mount APIRouter với prefix `/api/v1` |

---

## Điểm Rút Ra

- `AppException` handler bắt được tất cả subclass (`NotFoundException`, `BusinessException`) nhờ Python MRO — không cần đăng ký riêng từng loại
- Middleware chạy theo thứ tự đăng ký: CORS phải đăng ký trước logging để CORS header có trong preflight response
- `lifespan` thay `on_event` — code startup và cleanup nằm cùng 1 function, dễ đọc hơn và không bị mất cleanup khi exception

---

## Lỗi Gặp Phải

| # | Lỗi | Fix | Entry trong error-log |
|---|-----|-----|-----------------------|
| — | Không gặp lỗi trong phase này | — | — |
