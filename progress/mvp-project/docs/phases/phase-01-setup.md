# Phase 1 — Khởi Tạo Project

## Trạng Thái

- [x] Đang làm
- [x] Hoàn thành

**Bắt đầu:** 2026-05-31  
**Kết thúc:** 2026-05-31

---

## Tổng Quan Phase Này

**Làm gì:** Tạo skeleton project — cài dependencies, cấu hình env, viết config.py và database.py.

**Tại sao làm trước:** Tất cả các layer sau (models, schemas, routers) đều import từ `config.py` và `database.py`.
Nếu 2 file này chưa có hoặc sai → không verify được bất kỳ thứ gì.

**Kết quả mong đợi:** Chạy `uv run python -c "from app.core.database import engine; print('OK')"` → in ra `OK`.

---

## Các Bước Thực Hiện

### Bước 1.1 — Khởi tạo project với uv

**Làm gì:**
```bash
mkdir finance-tracker && cd finance-tracker
uv init .
uv add fastapi uvicorn[standard] sqlalchemy[asyncio] aiosqlite alembic pydantic-settings
uv add --dev httpx pytest ruff
```

**Tại sao dùng uv thay vì pip?**
- `uv` nhanh hơn pip 10–100x
- `uv.lock` đảm bảo mọi người cài đúng version
- `uv run` tự activate venv → không cần `source venv/bin/activate`

**Kiến thức áp dụng:** Khối 11 — package management

**Kết quả verify:**
```bash
uv run python -c "import fastapi, sqlalchemy, alembic; print('OK')"
# Mong đợi: OK
```

**Kết quả thực tế:** `sqlite+aiosqlite:///./finance.db` — PASS

---

### Bước 1.2 — Tạo cấu trúc thư mục

**Làm gì:**
```bash
mkdir -p app/{core,models,schemas,repositories,routers}
touch app/__init__.py app/core/__init__.py app/models/__init__.py
touch app/schemas/__init__.py app/repositories/__init__.py app/routers/__init__.py
```

**Tại sao cần `__init__.py`?**
Python coi thư mục là package khi có `__init__.py`.
Thiếu file này → `from app.core.config import Settings` sẽ lỗi `ModuleNotFoundError`.

**Kiến thức áp dụng:** Khối 4 — Python modules/packages

---

### Bước 1.3 — Tạo .env và config.py

**Làm gì:** Tạo `.env` với DATABASE_URL, sau đó viết `app/core/config.py` dùng pydantic-settings để đọc.

**Tại sao không hardcode URL trong code?**
- `.env` không commit lên git → bảo mật
- Dễ switch giữa SQLite (dev) và PostgreSQL (prod) bằng cách đổi env var

**Kiến thức áp dụng:** Khối 5 — Pydantic Settings, Khối 11 — database config

**Lỗi gặp phải:** *(ghi vào đây nếu có, chi tiết hơn ở errors/error-log.md)*

---

### Bước 1.4 — Viết database.py

**Làm gì:** Tạo `create_async_engine`, `async_sessionmaker`, và `get_db()` generator.

**Tại sao dùng generator (yield) cho get_db?**
- `yield` tạo context — code sau yield chạy khi request kết thúc
- Đảm bảo session luôn được close, kể cả khi có exception
- `try/finally` pattern → rollback nếu lỗi, commit nếu thành công

**Kiến thức áp dụng:** Khối 11 — AsyncSession, Depends với yield

---

## Kiến Thức Áp Dụng Trong Phase Này

| Kiến thức | Áp dụng cụ thể |
|----------|---------------|
| pydantic-settings | `Settings` class đọc từ `.env` |
| `create_async_engine` | Kết nối DB theo kiểu async |
| `async_sessionmaker` | Factory tạo session cho mỗi request |
| `Depends(get_db)` | Inject session vào router |

---

## Điểm Rút Ra

- `uv` tự tạo `.venv` trong project khi chạy lần đầu — không cần `python -m venv` thủ công
- Biến `VIRTUAL_ENV` trong shell (từ conda/brew) gây warning nhưng không ảnh hưởng — `uv` tự ignore và dùng `.venv` của project
- `expire_on_commit=False` trong `async_sessionmaker` quan trọng — không có nó, truy cập object sau `commit()` sẽ trigger thêm query (lazy reload)

---

## Lỗi Gặp Phải

*(Ghi ngắn gọn ở đây, chi tiết xem [error-log.md](../errors/error-log.md))*

| # | Lỗi | Fix | Entry trong error-log |
|---|-----|-----|-----------------------|
| | | | |
