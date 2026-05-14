# Lộ Trình Học Python & FastAPI
> Dành cho developer đã có kinh nghiệm lập trình (PHP/Laravel, Java Spring, Flutter)
> Phiên bản: Python 3.12+ | FastAPI 0.136+
> Thời gian ước tính: ~1 tuần (học song song công việc, ~3-4h/ngày)

---

## PHASE 1 — NỀN TẢNG PYTHON

---

### 🟦 Khối 1 — Làm Quen Môi Trường & Kiểu Dữ Liệu Cơ Bản

```
Giới thiệu Python: Vị trí trong hệ sinh thái backend hiện đại
Cài đặt Python 3.12, pyenv và cấu hình môi trường ảo (venv)
Tổng quan cú pháp Python: Indentation, comment, cách chạy file .py
Kiểu số Number: int, float, complex và phép toán số học
Kiểu Boolean và lý luận logic trong Python
Phép so sánh và toán tử logic (and, or, not, is, in)
Phép gán kết hợp: Assignment Operators (+=, -=, **=, //=)
```

---

### 🟦 Khối 2 — Kiểm Soát Luồng

```
Mệnh đề điều kiện if / elif / else
Vòng lặp While và cơ chế dừng vòng lặp
Sử dụng For để duyệt phần tử trong Container
Sự khác biệt giữa Continue và Break
Xây dựng dãy số với Range
Comprehension Expression: List, Dict, Set comprehension một dòng
Toán tử ba ngôi (Ternary Operator) trong Python
```

---

### 🟦 Khối 3 — String & Container

```
Tìm hiểu đối tượng String: Tính bất biến (immutable) và indexing
Các phương thức xử lý String thường dùng (upper, lower, strip, replace)
Sử dụng Split và Join để thao tác với String
Tìm hiểu phương thức Format: f-string, .format(), % operator
Tìm hiểu đối tượng List: Khởi tạo, truy cập, slicing
Các phương thức xử lý với List (append, extend, insert, remove, pop, sort)
Tìm hiểu Queue và Stack khi dùng List
List Comprehension và tối ưu mã nguồn
Tìm hiểu đối tượng Tuple: Bất biến và khi nào nên dùng
Tìm hiểu đối tượng Set: Phép hội, giao, hiệu
Tìm hiểu đối tượng Dictionary: Khởi tạo, truy cập, cập nhật
Các phương thức quan trọng của Dictionary (keys, values, items, get, setdefault)
```

---

### 🟦 Khối 4 — Hàm & Iterator

```
Hướng dẫn xây dựng hàm trong Python
Hàm và tham số: positional, keyword, default value
Tìm hiểu *args và **kwargs (More Parameters)
Hàm Lambda (Anonymous Function)
Các hàm built-in quan trọng: map, filter, sorted, enumerate, zip
Tìm hiểu Scope biến: Local, Global, Nonlocal
Tìm hiểu Iterator và giao thức __iter__ / __next__
Generator Function và từ khóa yield
Decorator trong Python: Khái niệm và ứng dụng thực tế
Bài tập tổng hợp về xây dựng hàm P1
Bài tập tổng hợp về xây dựng hàm P2
```

---

### 🟦 Khối 5 — Lập Trình Hướng Đối Tượng (OOP)

```
Giới thiệu OOP trong Python: So sánh với Java và PHP
Xây dựng Class và Object: Thuộc tính và phương thức
Tìm hiểu Constructor (__init__) và Destructor (__del__)
Tính đóng gói: Public, Protected, Private trong Python
Tìm hiểu tính kế thừa P1: Đơn kế thừa
Tìm hiểu tính kế thừa P2: Override và super()
Đa kế thừa (Multiple Inheritance) và MRO (Method Resolution Order)
Tính đa hình (Polymorphism) và Duck Typing
Dunder Methods: __str__, __repr__, __len__, __eq__
Dataclass trong Python: Thay thế class thuần túy lưu dữ liệu
```

---

### 🟦 Khối 6 — File, Module, Exception

```
Quy trình đọc File: open(), with statement, các chế độ r/w/a/b
Thực hiện ghi File và tối ưu hóa bằng Buffer
Đọc và ghi file JSON, CSV trong Python
Giới thiệu Module: import, from...import, alias
Các Module có sẵn quan trọng: os, sys, pathlib, datetime, json, re
Tự xây dựng Package và Module cho dự án
Quản lý và xử lý lỗi với Exception Handling P1: try/except/finally
Quản lý và xử lý lỗi với Exception Handling P2: Custom Exception
```

---

## PHASE 2 — PYTHON NÂNG CAO CHO FASTAPI

---

### 🟨 Khối 7 — Type Hints & Async Programming

```
Giới thiệu Type Hints trong Python 3.10+: int, str, list, dict, Optional
Union, Optional, Any và cú pháp X | Y
Annotating function: Khai báo kiểu cho tham số và return type
Generic Types: List[T], Dict[K, V], Tuple[T, ...]
TypedDict và NamedTuple: Khai báo cấu trúc dữ liệu có kiểu
Giới thiệu Asynchronous Programming: Tại sao cần async trong API
Tìm hiểu asyncio: Event loop, coroutine, Task
Từ khóa async def và await: Viết hàm bất đồng bộ
So sánh Blocking vs Non-blocking I/O
Bài tập async: Gọi nhiều API đồng thời bằng asyncio.gather
```

---

### 🟨 Khối 8 — Pydantic & Quản Lý Phụ Thuộc

```
Giới thiệu Pydantic v2: Tại sao FastAPI phụ thuộc Pydantic
Xây dựng BaseModel: Khai báo schema dữ liệu
Validation tự động: Kiểu dữ liệu, giá trị mặc định, required fields
Field() và các tùy chọn: alias, gt, lt, min_length, max_length
Nested Model: Model lồng nhau và List of Models
Model Validator: @model_validator và @field_validator
Serialization: model.model_dump(), model_dump_json()
Pydantic Settings: Quản lý cấu hình từ .env file
Giới thiệu pip, pip-tools và quản lý requirements.txt
Giới thiệu uv: Công cụ quản lý package mới nhất thay thế pip
```

---

## PHASE 3 — FASTAPI CƠ BẢN

---

### 🟩 Khối 9 — Làm Quen FastAPI & Routing

```
Giới thiệu FastAPI: Hiệu năng, OpenAPI tự động, so sánh với Flask/Django
Cài đặt FastAPI, Uvicorn và chạy Hello World
Khám phá Swagger UI (/docs) và ReDoc (/redoc)
Tìm hiểu Path Operation: @app.get, @app.post, @app.put, @app.delete
Path Parameters: Khai báo và validate tham số trong URL
Query Parameters: Tham số tùy chọn và giá trị mặc định
Request Body: Nhận JSON data qua Pydantic Model
Kết hợp Path + Query + Body trong một endpoint
Response Model: Khai báo schema trả về với response_model
HTTP Status Codes: Trả về mã lỗi chuẩn (201, 400, 404, 422, 500)
```

---

### 🟩 Khối 10 — Request & Response Nâng Cao

```
Form Data và File Upload trong FastAPI
Request Headers và Cookies: Đọc và sử dụng
HTTPException: Ném lỗi có cấu trúc về client
Custom Exception Handler: Xử lý lỗi toàn cục
Response trực tiếp: JSONResponse, HTMLResponse, FileResponse
Background Tasks: Thực hiện tác vụ nền sau khi trả response
APIRouter: Tách route theo module (tương tự Blueprint trong Flask)
Tổ chức cấu trúc thư mục dự án FastAPI chuẩn
CORS Middleware: Cấu hình cho phép frontend gọi API
Middleware tự xây dựng: Logging, request timing
```

---

### 🟩 Khối 11 — Dependency Injection & Database

```
Giới thiệu Dependency Injection (DI) trong FastAPI
Xây dựng Dependency đơn giản với Depends()
Dependency lồng nhau (Nested Dependencies)
Dependency chia sẻ trạng thái: Singleton pattern trong DI
Giới thiệu SQLAlchemy 2.0: ORM hiện đại cho Python
Kết nối Database: PostgreSQL/MySQL (prod)
Định nghĩa Model ORM với SQLAlchemy DeclarativeBase
Session Management: Dependency cung cấp DB session
Thực hiện CRUD cơ bản: Create, Read, Update, Delete qua ORM
Async SQLAlchemy: Kết hợp asyncpg và async session
Alembic: Migration database (tương tự Flyway trong Java)
Xây dựng API CRUD hoàn chỉnh: Ví dụ thực tế Product API
```

---

## PHASE 4 — FASTAPI NÂNG CAO

---

### 🟧 Khối 12 — Authentication & Security

```
Giới thiệu bảo mật API: OAuth2, JWT, API Key
OAuth2PasswordBearer: Cơ chế xác thực bằng Bearer token
Xây dựng endpoint đăng nhập: Kiểm tra user, tạo JWT token
JWT Token: Cấu trúc Header.Payload.Signature, thư viện python-jose
Dependency xác thực: get_current_user từ JWT token
Phân quyền theo role (RBAC): Admin, User, Guest
Refresh Token: Cơ chế làm mới token hết hạn
Password Hashing: bcrypt và passlib
API Key Authentication: Xác thực bằng header X-API-Key
HTTPS và các security best practices trong production
```

---

### 🟧 Khối 13 — Testing & Chất Lượng Code

```
Giới thiệu pytest: Framework test tiêu chuẩn Python
Viết Unit Test cơ bản cho hàm Python thuần
TestClient của FastAPI: Gọi API trong test mà không cần server thật
Fixture trong pytest: Setup và teardown dữ liệu test
Test Database: Sử dụng SQLite in-memory cho môi trường test
Mocking với unittest.mock: Giả lập phụ thuộc bên ngoài
Test Authentication: Kiểm tra endpoint có bảo vệ
Coverage Report: Đo độ phủ test với pytest-cov
Tổ chức test theo cấu trúc dự án: tests/ folder
Code quality: ruff (linter), black (formatter), mypy (type check)
```

---

### 🟧 Khối 14 — Triển Khai & Vận Hành (Có thể học thêm - tự học)

```
Cấu hình môi trường: .env file, Pydantic Settings, dev/staging/prod
Gunicorn + Uvicorn Worker: Chạy FastAPI production-ready
Dockerize ứng dụng FastAPI: Viết Dockerfile tối ưu
Docker Compose: Kết hợp FastAPI + PostgreSQL + Redis
Health Check Endpoint: /health và /readiness
Logging chuẩn: structlog hoặc Python logging với JSON output
Tích hợp Jenkins CI: Build, test, lint tự động
Triển khai lên Linux server: systemd service hoặc Docker
Reverse Proxy với Nginx: Forward request đến FastAPI
Monitoring cơ bản: Prometheus metrics endpoint
```

---

### 🟧 Khối 15 — Chủ Đề Chuyên Sâu (Có thể học thêm - tự học)

```
Async Background Jobs: Celery + Redis Queue
WebSocket trong FastAPI: Real-time communication
Server-Sent Events (SSE): Streaming response
Rate Limiting: Giới hạn số lượng request từ client
Caching với Redis: Cache endpoint response
File handling nâng cao: Upload lên S3/MinIO
GraphQL với Strawberry: Thay thế REST API khi cần
Microservice Pattern: Giao tiếp giữa các FastAPI service qua HTTP/gRPC
FastAPI với MongoDB: Motor async driver
Tích hợp AI/LLM: Gọi Anthropic/OpenAI API từ FastAPI service
```

---

## PHỤ LỤC

### Tài Nguyên Học Tập

| Nguồn | Nội dung | Link |
|---|---|---|
| FastAPI Official Docs | Tutorial đầy đủ, chuẩn nhất | https://fastapi.tiangolo.com |
| Pydantic v2 Docs | Validation và serialization | https://docs.pydantic.dev |
| SQLAlchemy 2.0 | ORM và async | https://docs.sqlalchemy.org |
| Real Python | Bài viết chuyên sâu Python | https://realpython.com |
| TestDriven.io | FastAPI + Testing + Docker | https://testdriven.io |

---

### Stack Công Nghệ Đề Xuất (Production)

```
Runtime      : Python 3.12+
Framework    : FastAPI 0.136+
Server       : Uvicorn (dev) + Gunicorn (prod)
ORM          : SQLAlchemy 2.0 async
Validation   : Pydantic v2
Database     : PostgreSQL (prod)
Migration    : Alembic
Auth         : python-jose (JWT) + passlib (bcrypt)
Testing      : pytest + httpx (async TestClient)
Linter       : ruff + mypy
Container    : Docker + Docker Compose
CI           : Jenkins (tích hợp hệ thống hiện có của Digi Dinos)
```

---

### Ghi Chú Cho Người Hướng Dẫn

> **Khối 1–6** — Học viên đã có kinh nghiệm lập trình, nên đẩy nhanh tốc độ. Tập trung vào điểm khác biệt của Python so với PHP/Java (indentation thay braces, duck typing, GIL).
>
> **Khối 7–8** — **Quan trọng nhất** trước khi học FastAPI. Không hiểu Type Hints và Pydantic sẽ bị mù khi đọc code FastAPI.
>
> **Khối 9–11** — Core của FastAPI. Hoàn thành khối này là có thể xây REST API đủ dùng cho dự án thực tế.
>
> **Khối 12–15** — Học theo nhu cầu dự án thực tế, không cần học tuần tự.
