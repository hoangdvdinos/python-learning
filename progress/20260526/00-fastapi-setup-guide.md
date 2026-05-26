# 00 — Set Up Môi Trường & Chạy FastAPI

> **Mục tiêu:** Hiểu *tại sao* mỗi bước tồn tại, không chỉ copy-paste lệnh.  
> **Góc nhìn:** So sánh với Spring Boot để bạn bắt được pattern ngay.

---

## Tổng Quan — Stack So Sánh

```
Spring Boot stack                FastAPI stack
─────────────────────            ──────────────────────────
Java 21                          Python 3.12+
Maven / Gradle                   uv  (package manager)
pom.xml / build.gradle           pyproject.toml  (manifest)
.m2 local repo (global cache)    ~/.cache/uv     (global cache)
per-project classpath            venv  (isolated env)
spring-boot-starter-web          fastapi + uvicorn[standard]
Tomcat (WSGI-like, blocking)     Uvicorn (ASGI, async-native)
mvn spring-boot:run              uvicorn main:app --reload
http://localhost:8080            http://localhost:8000
```

---

## Bước 0 — Kiểm Tra Python Đã Có Chưa

```powershell
python --version
# Cần: Python 3.12.x (stable release)
# Tại sao 3.12+: FastAPI dùng `type | None` syntax thay `Optional[type]`
#                 và match statement — tất cả cần 3.10+. 3.12 là LTS ổn định nhất.
```

> ⚠️ **TRÁNH Python Alpha/Beta** (ví dụ: 3.15.0b1, 3.14a2):  
> Phiên bản beta chưa có **pre-built wheel** trên Windows → pip/uv phải compile từ source  
> → cần Microsoft C++ Build Tools (~5GB) → phần lớn packages sẽ **báo lỗi build**.  
> **Luôn dùng stable release** — kiểm tra tại https://python.org/downloads/  
> (stable = không có chữ `a`, `b`, `rc` sau số version)

### Nếu máy đã lỡ cài Python beta — dùng uv để cài stable

```powershell
# uv tự tải Python 3.12 stable, không ảnh hưởng Python đã có
uv python install 3.12

# Gắn project dùng Python 3.12
uv python pin 3.12

# Xóa venv cũ (nếu đã tạo với Python beta), tạo lại
Remove-Item -Recurse -Force .venv
uv sync
```

> uv quản lý Python riêng trong `~/.local/share/uv/python/` — các phiên bản sống song song,  
> mỗi project chọn phiên bản qua file `.python-version`.

---

## Bước 1 — Cài `uv` (Package Manager)

### Tại sao cần uv? Không dùng pip thẳng được sao?

`pip` là công cụ mặc định của Python — giống như tự tải file `.jar` và thêm vào classpath tay.  
**`uv`** = Maven/Gradle cho Python:

| Tính năng | pip | uv |
|-----------|-----|----|
| Cài package | ✅ | ✅ |
| Lock file (reproducible builds) | ❌ (cần pip-tools riêng) | ✅ tự động |
| Tạo virtual env | ❌ (cần `python -m venv` riêng) | ✅ tự động |
| Tốc độ | chậm | **10-100x nhanh hơn** (viết bằng Rust) |
| Quản lý Python version | ❌ | ✅ |

```powershell
# Cài uv trên Windows (chạy 1 lần duy nhất trên máy)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Kiểm tra đã cài thành công
uv --version
# Output dạng: uv 0.5.x (...)
```

> `irm` = `Invoke-RestMethod` — tải script từ URL  
> `iex` = `Invoke-Expression` — chạy script vừa tải  
> Lệnh này tải binary uv về `~/.cargo/bin/uv` và thêm vào PATH tự động.

---

## Bước 2 — Tạo Project Mới

### 2.1 Khởi tạo project

```powershell
# Đặt tên project là "my-api" — uv tự tạo thư mục
uv init my-api

# Kết quả — uv tạo cấu trúc này:
# my-api/
# ├── .venv/              ← virtual environment (tương đương .m2 riêng cho project)
# ├── .python-version     ← ghi phiên bản Python project dùng
# ├── pyproject.toml      ← tương đương pom.xml
# ├── README.md
# └── hello.py            ← file mẫu, xóa sau

cd my-api
```

### 2.2 `pyproject.toml` là gì?

```toml
# pyproject.toml — tương đương pom.xml trong Maven
[project]
name = "my-api"
version = "0.1.0"
requires-python = ">=3.12"     # ← như <java.version>21</java.version>
dependencies = []               # ← uv tự thêm khi bạn chạy uv add

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

> **Khác Maven:** Không cần khai báo tay — uv tự sửa file này khi bạn thêm/xóa package.

---

## Bước 3 — Cài Packages FastAPI

```powershell
# Cài các package cần cho production
uv add fastapi "uvicorn[standard]" pydantic-settings

# Cài thêm package chỉ dùng khi dev/test (tương đương Maven <scope>test</scope>)
uv add --dev httpx pytest ruff mypy
```

### Giải thích từng package:

| Package | Vai trò | Tương đương Java |
|---------|---------|-----------------|
| `fastapi` | Framework chính — routing, validation, docs | `spring-boot-starter-web` |
| `uvicorn` | ASGI server — nhận HTTP request, chạy Python app | Tomcat / Netty |
| `uvicorn[standard]` | uvicorn + thêm: `websockets`, `httptools` (tốc độ), `python-dotenv` | Tomcat full bundle |
| `pydantic-settings` | Đọc config từ `.env` file và environment variable | `@ConfigurationProperties` + `@Value` |
| `httpx` | HTTP client async — dùng trong code và test | `WebClient` (Spring WebFlux) |
| `pytest` | Test framework | JUnit 5 |
| `ruff` | Linter + formatter (siêu nhanh) | Checkstyle + SpotBugs |
| `mypy` | Static type checker | Java compiler type checks |

> Sau khi `uv add`, kiểm tra `pyproject.toml` — bạn sẽ thấy các package đã được thêm vào `dependencies`.  
> Đồng thời `uv.lock` được tạo — **commit file này** vào git, tương đương `pom.xml` với version lock.

---

## Bước 4 — Hiểu Virtual Environment (venv)

### Tại sao cần venv?

Hãy tưởng tượng bạn có 2 project:
- Project A cần `fastapi==0.100.0`  
- Project B cần `fastapi==0.136.0`

Nếu cài global → conflict. **venv** cách ly mỗi project có bộ package riêng — giống như mỗi project Maven có classpath riêng, không dùng chung global.

```
Máy của bạn
├── ~/.cache/uv/            ← uv cache global (download 1 lần, dùng nhiều nơi)
│
├── my-api/
│   └── .venv/              ← môi trường RIÊNG của my-api
│       └── Lib/site-packages/fastapi==0.136.0
│
└── old-project/
    └── .venv/              ← môi trường RIÊNG của old-project
        └── Lib/site-packages/fastapi==0.100.0
```

> `uv init` đã tự tạo `.venv/` cho bạn — không cần làm thêm gì.

### Kích hoạt venv (Windows PowerShell)

```powershell
# Kích hoạt — cần làm mỗi khi mở terminal mới
.venv\Scripts\Activate.ps1

# Bạn biết đã kích hoạt khi thấy prefix trong terminal:
# (my-api) PS D:\hoangdv\my-api>
#  ↑ tên venv

# Tắt kích hoạt
deactivate
```

> **Với `uv run`:** Bạn có thể **bỏ qua kích hoạt venv** — `uv run` tự dùng `.venv` của project.  
> Dùng `uv run` là cách khuyến khích vì không phụ thuộc vào trạng thái terminal.

---

## Bước 5 — Tạo File `main.py`

```powershell
# Xóa file mẫu của uv (không cần thiết)
Remove-Item hello.py

# Tạo file main.py (hoặc tạo từ IDE)
New-Item main.py
```

Nội dung `main.py` tối thiểu để chạy được:

```python
# main.py
from fastapi import FastAPI

# Tạo instance FastAPI — tương đương @SpringBootApplication
# title, description, version → hiển thị trong /docs
app = FastAPI(
    title="My API",
    version="1.0.0",
    description="API demo cho Java developer",
)

# Endpoint đầu tiên
# @app.get("/") = @GetMapping("/") trong @RestController
@app.get("/")
async def root():
    # Trả dict → FastAPI tự chuyển thành JSON + set Content-Type: application/json
    return {"message": "Hello FastAPI", "status": "running"}
```

---

## Bước 6 — Chạy Server

### 6.1 Lệnh chạy — giải thích từng phần

```powershell
uvicorn main:app --reload
#        ↑    ↑    ↑
#        │    │    └── Auto-restart khi code thay đổi (dev only — như Spring DevTools)
#        │    └─────── Tên biến FastAPI trong file (app = FastAPI())
#        └──────────── Tên file Python KHÔNG có .py (main.py → main)
```

**Hoặc dùng `uv run`** (khuyến khích — không cần kích hoạt venv):

```powershell
uv run uvicorn main:app --reload
```

### 6.2 Output khi chạy thành công

```
INFO:     Will watch for changes in these directories: ['D:\\hoangdv\\my-api']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

> Không thấy lỗi đỏ = server đã chạy.  
> `Press CTRL+C to quit` — dừng server.

### 6.3 Tùy chọn nâng cao khi chạy

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8080 --log-level debug
#                          ↑               ↑            ↑
#                          │               │            └── Log chi tiết hơn
#                          │               └────────────── Đổi port (default: 8000)
#                          └────────────────────────────── Cho phép truy cập từ network ngoài
#                                                          (default 127.0.0.1 = localhost only)
```

---

## Bước 7 — Kiểm Tra Server Đang Chạy

Mở browser và truy cập:

| URL | Nội dung | Tương đương |
|-----|----------|-------------|
| `http://localhost:8000` | API endpoint (bạn vừa code) | API endpoint |
| `http://localhost:8000/docs` | **Swagger UI** — test ngay trên browser | Postman + Swagger |
| `http://localhost:8000/redoc` | **ReDoc** — docs dạng đọc | Javadoc đẹp hơn |
| `http://localhost:8000/openapi.json` | OpenAPI JSON schema | Contract file |

> **Không cần config gì thêm** — FastAPI tự sinh `/docs` và `/redoc` từ code của bạn.  
> Với Spring Boot bạn cần thêm `springdoc-openapi` dependency + config → đây là ưu điểm lớn của FastAPI.

---

## Bước 8 — Cấu Trúc Project Khuyến Khích

```
my-api/
├── .venv/                  ← venv — KHÔNG commit vào git
├── .gitignore              ← thêm .venv/ vào đây
├── pyproject.toml          ← commit — tương đương pom.xml
├── uv.lock                 ← commit — lock file đảm bảo mọi người cài cùng version
│
├── main.py                 ← entry point — uvicorn main:app
│
├── app/                    ← source chính (tương đương src/main/java)
│   ├── __init__.py         ← đánh dấu đây là Python package (như package-info.java)
│   ├── routers/            ← routes theo domain (tương đương @RestController classes)
│   │   ├── __init__.py
│   │   ├── users.py        ← /users endpoints
│   │   └── products.py     ← /products endpoints
│   ├── models/             ← Pydantic schemas (tương đương DTO classes)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── product.py
│   ├── services/           ← business logic (tương đương @Service)
│   │   └── user_service.py
│   └── config.py           ← settings (tương đương application.properties)
│
└── tests/                  ← tests (tương đương src/test/java)
    ├── __init__.py
    └── test_users.py
```

> **Giai đoạn học:** Chỉ cần `main.py` là đủ, không cần structure phức tạp ngay.  
> **Khi project lớn hơn:** Tách dần ra theo structure trên.

---

## Bước 9 — Chạy Với `--reload` và Thử Thay Đổi

1. Server đang chạy với `--reload`
2. Mở `main.py`, sửa `"Hello FastAPI"` thành `"Xin chào FastAPI"`
3. **Lưu file** (Ctrl+S)
4. Terminal sẽ tự hiện:
   ```
   WARNING:  StatReload detected changes in 'main.py'. Reloading...
   INFO:     Application startup complete.
   ```
5. Refresh browser `http://localhost:8000` → thấy ngay giá trị mới

> Giống Spring Boot DevTools nhưng **nhanh hơn** — reload trong ~0.5s thay vì vài giây.

---

## Bước 10 — `.gitignore` Cần Có

```powershell
# Tạo .gitignore
New-Item .gitignore
```

Nội dung tối thiểu:

```gitignore
# Virtual environment — KHÔNG bao giờ commit
.venv/

# Python cache
__pycache__/
*.pyc
*.pyo
.mypy_cache/
.ruff_cache/
.pytest_cache/

# IDE
.vscode/
.idea/

# Environment variables (chứa secret)
.env
.env.local
.env.production
```

> ⚠️ **`.venv/` phải có trong `.gitignore`** — giống như `target/` của Maven.  
> Teammate clone về chạy `uv sync` là đủ, không cần commit venv.

---

## Tóm Tắt Quy Trình — Clone Project Người Khác

```powershell
# 1. Clone project
git clone https://github.com/.../my-api.git
cd my-api

# 2. Cài đúng dependencies theo uv.lock (tương đương mvn install)
uv sync

# 3. Chạy
uv run uvicorn main:app --reload

# Xong — không cần cài thêm gì khác
```

---

## Troubleshooting — Lỗi Thường Gặp

### ❌ `ModuleNotFoundError: No module named 'fastapi'`

**Nguyên nhân:** Chạy Python nhưng không dùng venv đúng.

```powershell
# Sai — dùng Python global không có fastapi
python main.py

# Đúng — dùng uv (tự dùng .venv)
uv run uvicorn main:app --reload

# Hoặc kích hoạt venv trước
.venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

---

### ❌ `uvicorn: command not found` hoặc `uvicorn is not recognized`

**Nguyên nhân:** Venv chưa được kích hoạt và không dùng `uv run`.

```powershell
# Cách 1: dùng uv run
uv run uvicorn main:app --reload

# Cách 2: kích hoạt venv
.venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

---

### ❌ `Error: [Errno 10048] Only one usage of each socket address`

**Nguyên nhân:** Port 8000 đã có process khác dùng (thường là server cũ chưa tắt).

```powershell
# Tìm process đang dùng port 8000
netstat -ano | Select-String ":8000"

# Tắt process theo PID (thay 12345 bằng PID thực)
Stop-Process -Id 12345 -Force

# Hoặc đổi port
uvicorn main:app --reload --port 8001
```

---

### ❌ `SyntaxError: invalid syntax` ngay khi start

**Nguyên nhân:** Python version sai (cần 3.10+ cho `type | None` syntax, 3.12+ khuyến khích).

```powershell
# Kiểm tra version đang dùng
python --version

# Kiểm tra version trong venv
.venv\Scripts\python.exe --version

# uv tự dùng version khai báo trong .python-version
cat .python-version
```

---

### ❌ `404 Not Found` khi truy cập endpoint

**Nguyên nhân:** URL sai hoặc route khai báo sai.

```powershell
# Kiểm tra danh sách routes trong /docs
# http://localhost:8000/docs

# Hoặc xem openapi.json
# http://localhost:8000/openapi.json
```

---

## Cheat Sheet — Lệnh Hay Dùng

```powershell
# ── Setup (1 lần) ──────────────────────────────────────────
uv init my-api                           # Tạo project mới
uv add fastapi "uvicorn[standard]"       # Thêm dependency
uv add --dev pytest httpx ruff           # Thêm dev dependency
uv sync                                  # Cài từ uv.lock (clone về)

# ── Chạy ───────────────────────────────────────────────────
uv run uvicorn main:app --reload         # Dev server
uv run uvicorn main:app --reload --port 8001  # Đổi port

# ── Package management ─────────────────────────────────────
uv add requests                          # Thêm package
uv remove requests                       # Xóa package
uv pip list                              # Xem packages đã cài

# ── Chạy script/test ───────────────────────────────────────
uv run python main.py                    # Chạy script
uv run pytest                            # Chạy test
uv run ruff check .                      # Lint code
uv run mypy .                            # Type check
```

---

## Bước Tiếp Theo

Sau khi setup xong và chạy được `http://localhost:8000/docs`:

1. ✅ **[09-fastapi-routing.md](09-fastapi-routing.md)** — Path/Query params, Request body, Response model  
2. ⬜ Dependency Injection trong FastAPI  
3. ⬜ Kết nối Database (SQLAlchemy async)  
4. ⬜ Authentication (JWT)
