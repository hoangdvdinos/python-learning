# 00 — Set Up Môi Trường & Chạy FastAPI trên macOS (Apple Silicon M1 Pro)

> **Mục tiêu:** Hiểu *tại sao* mỗi bước tồn tại, không chỉ copy-paste lệnh.  
> **Góc nhìn:** So sánh với Spring Boot để bạn bắt được pattern ngay.  
> **Máy:** macOS Sonoma / Ventura — Apple Silicon M1 Pro (arm64)

---

## ⚡ Đã Có Project Rồi — Chạy Ngay

> Dùng khi clone project về máy, hoặc mở lại project cũ chưa có `.venv`.

```zsh
cd /path/to/my-api        # 1. vào đúng thư mục project

uv sync                   # 2. tạo .venv + cài đúng packages theo uv.lock
                          #    (tương đương mvn install — chạy 1 lần sau khi clone)

uv run uvicorn main:app --reload   # 3. chạy server
```

| Sau bước | Kết quả |
|----------|---------|
| `uv sync` | Thư mục `.venv/` được tạo, mọi package đã cài đúng version |
| `uv run uvicorn ...` | Server chạy tại `http://localhost:8000` |
| Mở `/docs` | Swagger UI sẵn sàng, không cần config thêm |

> **Từ lần sau** khi `.venv` đã có rồi → chỉ cần bước 3 là đủ.

---

## Tổng Quan — Stack So Sánh

```
Spring Boot stack                FastAPI stack
─────────────────────            ──────────────────────────
Java 21                          Python 3.12+
Maven / Gradle                   uv  (package manager)
pom.xml / build.gradle           pyproject.toml  (manifest)
.m2 local repo (global cache)    ~/.cache/uv     (global cache)
per-project classpath            .venv/  (isolated per-project)
spring-boot-starter-web          fastapi + uvicorn[standard]
Tomcat (blocking, WSGI-like)     Uvicorn (ASGI, async-native)
mvn spring-boot:run              uvicorn main:app --reload
http://localhost:8080            http://localhost:8000
```

---

## 🍎 M1 Pro — Điều Bạn Cần Biết Trước

### Tại sao M1 Pro có điểm khác biệt?

M1 Pro dùng kiến trúc **arm64** (Apple Silicon) thay vì **x86_64** (Intel). Điều này ảnh hưởng:

| Tình huống | Giải thích |
|-----------|-----------|
| **Package có native extension** | Cần wheel được build cho `arm64`. `uv`/`pip` tự chọn đúng wheel — bạn không cần lo nếu dùng Python 3.12 stable. |
| **Rosetta 2** | macOS có thể chạy x86 binary qua Rosetta, nhưng **không cần** cho Python dev — hãy dùng native arm64 Python. |
| **Terminal mặc định** | macOS đi kèm **zsh** (không phải bash). Mọi lệnh trong guide này đều dùng zsh. |
| **Homebrew path** | Intel Mac: `/usr/local/` — M1 Mac: `/opt/homebrew/` — khác nhau, quan trọng khi debug PATH. |

> ✅ **Tóm lại:** Chỉ cần cài **Python 3.12 stable** và **uv** đúng cách, M1 Pro chạy FastAPI mượt — thậm chí nhanh hơn Intel nhờ kiến trúc mới.

---

## Bước 0 — Kiểm Tra Python Đã Có Chưa

```zsh
python3 --version
# Cần: Python 3.12.x (stable release)
# Tại sao 3.12+: FastAPI dùng `type | None` syntax thay `Optional[type]`
#                 và match statement — tất cả cần 3.10+. 3.12 là LTS ổn định nhất.

# macOS dùng python3 (không phải python)
# macOS có sẵn Python 3.x từ Xcode Command Line Tools — thường là 3.9/3.11
# → ĐỪNG dùng Python system này cho project — uv sẽ quản lý riêng
which python3
# /usr/bin/python3  ← đây là Python system của macOS, không nên đụng vào
```

> ⚠️ **TRÁNH Python Alpha/Beta** (ví dụ: 3.15.0b1, 3.14a2):  
> Phiên bản beta chưa có **pre-built wheel** → phải compile từ source  
> → nhiều package sẽ **báo lỗi build**.  
> **Luôn dùng stable release** — kiểm tra tại https://python.org/downloads/  
> (stable = không có chữ `a`, `b`, `rc` sau số version)

### Nếu đã lỡ cài Python beta — dùng uv để cài stable

```zsh
# uv tự tải Python 3.12 stable, không ảnh hưởng Python hệ thống
uv python install 3.12

# Gắn project dùng Python 3.12
uv python pin 3.12

# Xóa venv cũ, tạo lại sạch
rm -rf .venv
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
| Hỗ trợ arm64 (M1) | ✅ | ✅ native |

```zsh
# Cài uv trên macOS (chạy 1 lần duy nhất trên máy)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sau khi cài, nạp lại shell config để PATH có hiệu lực ngay
source ~/.zshrc
# Hoặc đóng terminal và mở lại

# Kiểm tra đã cài thành công
uv --version
# Output dạng: uv 0.5.x (aarch64-apple-darwin ...)
#                         ↑ phải thấy aarch64 = native M1
```

> `curl -LsSf` tải script cài đặt từ internet.  
> `| sh` chạy script đó ngay.  
> uv được cài vào `~/.local/bin/uv` và tự thêm vào PATH trong `~/.zshrc`.

### ⚠️ Nếu `uv` không tìm thấy sau khi cài

```zsh
# Kiểm tra PATH
echo $PATH | tr ':' '\n' | grep -E "uv|local/bin"

# Thêm thủ công nếu thiếu
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

uv --version  # thử lại
```

---

## Bước 2 — Tạo Project Mới

### 2.1 Khởi tạo project

```zsh
# Đặt tên project là "my-api" — uv tự tạo thư mục
uv init my-api

# Kết quả — uv tạo cấu trúc này:
# my-api/
# ├── .venv/              ← virtual environment (tương đương classpath riêng cho project)
# ├── .python-version     ← ghi phiên bản Python project dùng
# ├── pyproject.toml      ← tương đương pom.xml
# ├── README.md
# └── hello.py            ← file mẫu, xóa sau

cd my-api

# Xác nhận Python đang dùng là arm64 (M1 native)
uv run python -c "import platform; print(platform.machine())"
# Phải in ra: arm64
# Nếu thấy x86_64 → Python đang chạy qua Rosetta → cần cài lại Python native
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

```zsh
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

### Kiểm tra package đã cài đúng wheel arm64

```zsh
# Xem chi tiết uvicorn đã cài
uv pip show uvicorn

# Kiểm tra nhanh: import fastapi không lỗi
uv run python -c "import fastapi; print(fastapi.__version__)"
# Output: 0.136.x (hoặc version mới hơn)
```

---

## Bước 4 — Hiểu Virtual Environment (venv)

### Tại sao cần venv?

Hãy tưởng tượng bạn có 2 project:
- Project A cần `fastapi==0.100.0`  
- Project B cần `fastapi==0.136.0`

Nếu cài global → conflict. **venv** cách ly mỗi project có bộ package riêng — giống như mỗi project Maven có classpath riêng, không dùng chung global.

```
Máy của bạn (M1 Pro)
├── ~/.cache/uv/            ← uv cache global (download 1 lần, dùng nhiều nơi)
│
├── ~/projects/my-api/
│   └── .venv/              ← môi trường RIÊNG của my-api  (arm64)
│       └── lib/python3.12/site-packages/fastapi==0.136.0
│
└── ~/projects/old-project/
    └── .venv/              ← môi trường RIÊNG của old-project  (arm64)
        └── lib/python3.12/site-packages/fastapi==0.100.0
```

> `uv init` đã tự tạo `.venv/` cho bạn — không cần làm thêm gì.

### Kích hoạt venv trên macOS (zsh)

```zsh
# Kích hoạt — cần làm mỗi khi mở terminal mới
source .venv/bin/activate
# macOS dùng source + đường dẫn bin/activate (khác Windows dùng Scripts\Activate.ps1)

# Bạn biết đã kích hoạt khi thấy prefix trong terminal:
# (my-api) hoangdv@MacBook-Pro my-api %
#  ↑ tên venv

# Tắt kích hoạt
deactivate
```

> **Với `uv run`:** Bạn có thể **bỏ qua kích hoạt venv** — `uv run` tự dùng `.venv` của project.  
> Đây là cách **khuyến khích** vì không phụ thuộc vào trạng thái terminal.

---

## Bước 5 — Tạo File `main.py`

```zsh
# Xóa file mẫu của uv (không cần thiết)
rm hello.py

# Tạo file main.py
touch main.py
# Hoặc mở thẳng bằng VS Code:
code main.py
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

```zsh
uvicorn main:app --reload
#        ↑    ↑    ↑
#        │    │    └── Auto-restart khi code thay đổi (dev only — như Spring DevTools)
#        │    └─────── Tên biến FastAPI trong file (app = FastAPI())
#        └──────────── Tên file Python KHÔNG có .py (main.py → main)
```

**Hoặc dùng `uv run`** (khuyến khích — không cần kích hoạt venv):

```zsh
uv run uvicorn main:app --reload
```

### 6.2 Output khi chạy thành công

```
INFO:     Will watch for changes in these directories: ['/Users/hoangdv/my-api']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

> Không thấy lỗi đỏ = server đã chạy thành công.  
> `Press CTRL+C to quit` — dừng server.

### 6.3 Tùy chọn nâng cao khi chạy

```zsh
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
> Với Spring Boot bạn cần thêm `springdoc-openapi` dependency + config — đây là ưu điểm lớn của FastAPI.

---

## Bước 8 — Cấu Trúc Project Khuyến Khích

```
my-api/
├── .venv/                  ← venv — KHÔNG commit vào git
├── .gitignore              ← thêm .venv/ vào đây
├── .python-version         ← "3.12" — commit, đảm bảo mọi người dùng cùng version
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
3. **Lưu file** (⌘S)
4. Terminal sẽ tự hiện:
   ```
   WARNING:  StatReload detected changes in 'main.py'. Reloading...
   INFO:     Application startup complete.
   ```
5. Refresh browser `http://localhost:8000` → thấy ngay giá trị mới

> Giống Spring Boot DevTools nhưng **nhanh hơn** — reload trong ~0.5s thay vì vài giây.

---

## Bước 10 — `.gitignore` Cần Có

```zsh
# Tạo .gitignore
touch .gitignore
```

Nội dung tối thiểu cho macOS + Python:

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
*.swp

# Environment variables (chứa secret — KHÔNG bao giờ commit)
.env
.env.local
.env.staging
.env.production

# macOS specific — KHÔNG cần cho dự án
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
```

> ⚠️ **`.venv/` phải có trong `.gitignore`** — giống như `target/` của Maven.  
> ⚠️ **`.DS_Store`** — macOS tự tạo trong mọi thư mục, không có giá trị gì cho dự án.  
> Teammate clone về chạy `uv sync` là đủ, không cần commit venv.

---

## Tóm Tắt Quy Trình — Clone Project Người Khác

```zsh
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

## Troubleshooting — Lỗi Thường Gặp Trên macOS

### ❌ `ModuleNotFoundError: No module named 'fastapi'`

**Nguyên nhân:** Chạy Python system của macOS thay vì Python trong venv.

```zsh
# Sai — dùng Python system /usr/bin/python3 không có fastapi
python3 main.py

# Đúng — dùng uv (tự dùng .venv)
uv run uvicorn main:app --reload

# Hoặc kích hoạt venv trước
source .venv/bin/activate
uvicorn main:app --reload

# Kiểm tra đang dùng Python nào
which python3
# Phải là: .../my-api/.venv/bin/python3  (nếu đã activate)
# Không phải: /usr/bin/python3           (Python system)
```

---

### ❌ `uv: command not found` sau khi cài

**Nguyên nhân:** PATH chưa được cập nhật trong terminal hiện tại.

```zsh
# Cách 1: Nạp lại .zshrc
source ~/.zshrc

# Cách 2: Đóng terminal và mở terminal mới

# Cách 3: Chạy với đường dẫn tuyệt đối
~/.local/bin/uv --version

# Cách 4: Thêm thủ công vào PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

### ❌ `Address already in use` — Port 8000 bị chiếm

**Nguyên nhân:** Còn terminal khác đang chạy server, hoặc process cũ chưa tắt.

```zsh
# Tìm process đang dùng port 8000
lsof -i :8000
# Output:
# COMMAND   PID     USER   ...  NAME
# Python  12345  hoangdv   ...  *:8000

# Tắt process theo PID
kill -9 12345

# Hoặc tắt tất cả Python đang chạy trên port 8000
lsof -ti :8000 | xargs kill -9

# Hoặc đổi port
uvicorn main:app --reload --port 8001
```

---

### ❌ `zsh: permission denied: .venv/bin/activate`

**Nguyên nhân:** File activate không có quyền execute.

```zsh
# Cấp quyền execute
chmod +x .venv/bin/activate

# Thử lại
source .venv/bin/activate
```

---

### ❌ `Python 3.x.x` nhưng arm64 không nhận — Kiểm tra kiến trúc

```zsh
# Kiểm tra Python đang chạy trên kiến trúc nào
python3 -c "import platform; print(platform.machine())"
# Kỳ vọng: arm64
# Nếu thấy: x86_64 → đang chạy qua Rosetta

# Kiểm tra file binary
file $(which python3)
# arm64: Mach-O 64-bit executable arm64
# Rosetta: Mach-O 64-bit executable x86_64

# Fix — cài lại Python native arm64 qua uv
uv python install 3.12
uv python pin 3.12
rm -rf .venv
uv sync
```

---

### ❌ `SyntaxError: invalid syntax` ngay khi start

**Nguyên nhân:** Python version sai (cần 3.10+ cho `type | None` syntax).

```zsh
# Kiểm tra version đang dùng
python3 --version

# Kiểm tra version trong venv
.venv/bin/python3 --version

# Kiểm tra .python-version của project
cat .python-version
# Phải là: 3.12 (hoặc 3.12.x)

# Fix
uv python install 3.12
uv python pin 3.12
rm -rf .venv && uv sync
```

---

### ❌ `404 Not Found` khi truy cập endpoint

**Nguyên nhân:** URL sai hoặc route khai báo sai.

```zsh
# Xem tất cả routes đang có trong /docs
open http://localhost:8000/docs

# Hoặc xem openapi.json bằng terminal
curl http://localhost:8000/openapi.json | python3 -m json.tool
```

---

### ❌ Homebrew Python conflict

macOS có thể có nhiều Python: system (`/usr/bin`), Homebrew (`/opt/homebrew`), uv (`~/.local/share/uv`).

```zsh
# Xem tất cả Python đang có trên máy
which -a python3

# Thứ tự ưu tiên nên là:
# 1. .venv/bin/python3       (khi đã activate venv)
# 2. ~/.local/bin/python3    (uv managed — dùng cho uv run)
# 3. /opt/homebrew/bin/python3 (Homebrew — dùng cho tools global)
# 4. /usr/bin/python3          (macOS system — ĐỪNG đụng)

# Với uv run → luôn dùng Python trong .venv → không bao giờ bị conflict
uv run python3 --version
```

---

## Cheat Sheet — Lệnh Hay Dùng (macOS / zsh)

```zsh
# ── Setup (1 lần cho máy) ──────────────────────────────────
curl -LsSf https://astral.sh/uv/install.sh | sh  # Cài uv
source ~/.zshrc                                   # Nạp PATH

# ── Tạo project mới ────────────────────────────────────────
uv init my-api                           # Tạo project
cd my-api
uv add fastapi "uvicorn[standard]"       # Thêm dependency
uv add pydantic-settings
uv add --dev pytest httpx ruff mypy      # Thêm dev dependency

# ── Kích hoạt venv (nếu cần) ───────────────────────────────
source .venv/bin/activate                # Kích hoạt
deactivate                               # Tắt kích hoạt

# ── Chạy server ────────────────────────────────────────────
uv run uvicorn main:app --reload         # Dev server (khuyến khích)
uv run uvicorn main:app --reload --port 8001  # Đổi port

# ── Package management ─────────────────────────────────────
uv add requests                          # Thêm package
uv remove requests                       # Xóa package
uv pip list                              # Xem packages đã cài
uv sync                                  # Cài từ uv.lock (sau khi clone)

# ── Chạy script/test ───────────────────────────────────────
uv run python3 main.py                   # Chạy script
uv run pytest                            # Chạy test
uv run pytest -v                         # Test verbose
uv run ruff check .                      # Lint code
uv run ruff format .                     # Format code
uv run mypy .                            # Type check

# ── Debug M1 ───────────────────────────────────────────────
uv run python3 -c "import platform; print(platform.machine())"  # Kiểm tra arm64
lsof -i :8000                            # Ai đang dùng port 8000
lsof -ti :8000 | xargs kill -9           # Kill process trên port 8000
file $(which python3)                    # Kiểm tra kiến trúc binary
```

---

## Bước Tiếp Theo

Sau khi setup xong và chạy được `http://localhost:8000/docs`:

1. ✅ **[09-fastapi-routing.md](09-fastapi-routing.md)** — Path/Query params, Request body, Response model
2. ⬜ Dependency Injection trong FastAPI (`Depends()`)
3. ⬜ Kết nối Database (SQLAlchemy async + asyncpg)
4. ⬜ Authentication (JWT + OAuth2)
