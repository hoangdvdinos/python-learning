# Phase 6 — main.py

## Trạng Thái

- [ ] Đang làm
- [ ] Hoàn thành

**Bắt đầu:** ___________  
**Kết thúc:** ___________

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

**Làm gì:**
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    print("Shutting down...")
```

**Tại sao dùng lifespan thay vì `@app.on_event("startup")`?**
- `on_event` deprecated trong FastAPI >= 0.93
- Lifespan là context manager → startup và shutdown nằm cùng 1 chỗ, dễ đọc
- Cleanup luôn chạy ngay cả khi startup có exception

**Kiến thức áp dụng:** Khối 11 — async context manager

---

### Bước 6.2 — CORS Middleware

**Làm gì:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Tại sao cần CORS?**
Frontend (React/Vue) chạy trên port khác (3000 hoặc 5173) → browser block request theo same-origin policy.
CORS middleware thêm `Access-Control-Allow-Origin` header → browser cho phép.

**Kiến thức áp dụng:** Khối 10 — Middleware

---

### Bước 6.3 — Request Logging Middleware

**Làm gì:**
```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"{request.method} {request.url.path} -> {response.status_code} ({duration:.3f}s)")
    return response
```

**Tại sao thêm X-Request-Id header?**
Khi có nhiều requests đồng thời, log dễ bị lẫn.
`X-Request-Id` cho phép trace 1 request end-to-end qua logs.

**Kiến thức áp dụng:** Khối 10 — Custom middleware

---

### Bước 6.4 — Exception Handlers

**Làm gì:** Register handler cho `NotFoundException`, `BusinessException`, và `Exception` chung.

**Thứ tự đăng ký quan trọng không?**
FastAPI check từ specific đến generic → đăng ký `NotFoundException` trước `Exception`.
Nếu chỉ đăng ký `Exception` → tất cả lỗi đều trả 500, mất thông tin.

**Kiến thức áp dụng:** Khối 10 — Exception handlers

---

## Kiến Thức Áp Dụng Trong Phase Này

| Kiến thức | Áp dụng cụ thể |
|----------|---------------|
| `@asynccontextmanager` | Lifespan startup/shutdown |
| `CORSMiddleware` | Cross-Origin Resource Sharing |
| `@app.middleware("http")` | Request/response logging |
| `app.add_exception_handler()` | Convert custom exceptions → HTTP response |
| `app.include_router()` | Mount APIRouter với prefix |

---

## Điểm Rút Ra

*(Ghi sau khi hoàn thành phase)*

- 
- 
- 

---

## Lỗi Gặp Phải

| # | Lỗi | Fix | Entry trong error-log |
|---|-----|-----|-----------------------|
| | | | |
