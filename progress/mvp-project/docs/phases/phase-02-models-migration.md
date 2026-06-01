# Phase 2 — ORM Models & Migration

## Trạng Thái

- [ ] Đang làm
- [x] Hoàn thành

**Bắt đầu:** 2026-05-31  
**Kết thúc:** 2026-05-31

---

## Tổng Quan Phase Này

**Làm gì:** Định nghĩa ORM models (Category, Transaction) và tạo database schema bằng Alembic.

**Tại sao làm trước schemas/routers?**
Schema (Pydantic) là "bản sao nhẹ" của Model (SQLAlchemy).
Phải biết model có những field gì → mới viết schema đúng được.
Nếu viết schema trước rồi model sau → rất dễ mismatch field name.

**Kết quả mong đợi:** `alembic upgrade head` tạo ra file `finance.db` với 2 bảng `categories` và `transactions`.

---

## Các Bước Thực Hiện

### Bước 2.1 — TimestampMixin

**Làm gì:** Viết `app/models/base.py` với `DeclarativeBase` và `TimestampMixin`.

**Tại sao dùng Mixin thay vì copy-paste?**
- `created_at`, `updated_at` lặp lại ở mọi model
- Mixin → thay đổi 1 chỗ, áp dụng cho tất cả
- `onupdate=func.now()` → DB tự cập nhật timestamp, không cần code manual

**Kiến thức áp dụng:** Khối 11 — SQLAlchemy 2.0, DeclarativeBase

**Lệnh:** *(không có lệnh shell — chỉ tạo file)*

---

### Bước 2.2 — Category Model

**Làm gì:** Viết `app/models/category.py`.

**Tại sao `Mapped[str | None]` cho `icon` và `color`?**
- `Mapped[str]` → NOT NULL trong DB
- `Mapped[str | None]` → nullable, client có thể không gửi
- SQLAlchemy 2.0 dùng type annotation thay vì `Column(nullable=True)` cũ

**Kiến thức áp dụng:** Khối 4 — Type hints, Khối 11 — Mapped[T]

**Lệnh:** *(không có lệnh shell — chỉ tạo file)*

---

### Bước 2.3 — Transaction Model

**Làm gì:** Viết `app/models/transaction.py` với ForeignKey tới categories.

**Tại sao cần `relationship("Category", lazy="selectin")`?**
- Khi query Transaction, cần hiển thị `category_name` trong response
- `lazy="selectin"` → SQLAlchemy tự JOIN, không cần viết JOIN thủ công
- Tránh N+1 problem: 10 transactions → 1 query, không phải 11 queries

**Kiến thức áp dụng:** Khối 11 — relationship, selectinload

**Lệnh:** *(không có lệnh shell — chỉ tạo file)*

---

### Bước 2.4 — `__init__.py` cho models

**Làm gì:** Import tất cả models vào `app/models/__init__.py`.

**Tại sao cần làm bước này?**
Alembic scan `target_metadata` để biết schema.
Nếu model chưa được import → Alembic không biết model tồn tại → không generate migration.
File này là "registration point" — phải import trước khi Alembic chạy.

**Lệnh:** *(không có lệnh shell — chỉ tạo file)*

---

### Bước 2.5 — Cấu hình Alembic

**Làm gì:** Khởi tạo Alembic, sửa `alembic.ini` và `alembic/env.py` để dùng async engine.

```bash
uv run alembic init alembic
```

Sau đó:
- Sửa `alembic.ini`: đổi `sqlalchemy.url` thành `sqlite+aiosqlite:///./finance.db`
- Viết lại `alembic/env.py`: dùng `async_engine_from_config` + `asyncio.run()` thay vì `engine_from_config` đồng bộ

**Tại sao `render_as_batch=True`?**
SQLite không support `ALTER TABLE ... ADD COLUMN` / `DROP COLUMN`.
`render_as_batch=True` khiến Alembic dùng cách khác: tạo bảng temp → copy data → drop bảng cũ → rename.
Nếu không bật → migration sẽ fail khi thay đổi schema trên SQLite.

**Kiến thức áp dụng:** Khối 11 — Alembic async config

---

### Bước 2.6 — Tạo và chạy migration

```bash
uv run alembic revision --autogenerate -m "init categories and transactions"
uv run alembic upgrade head
```

**Verify bảng đã được tạo:**

```bash
uv run python -c "
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
import sqlalchemy

async def check():
    engine = create_async_engine('sqlite+aiosqlite:///./finance.db')
    async with engine.connect() as conn:
        result = await conn.execute(sqlalchemy.text('SELECT name FROM sqlite_master WHERE type=\"table\"'))
        print([r[0] for r in result])
asyncio.run(check())
"
# Kết quả: ['alembic_version', 'categories', 'transactions']
```

**Verify schema chi tiết từng bảng:**

```bash
uv run python -c "
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
import sqlalchemy

async def check():
    engine = create_async_engine('sqlite+aiosqlite:///./finance.db')
    async with engine.connect() as conn:
        for tbl in ['categories', 'transactions']:
            result = await conn.execute(sqlalchemy.text(f'PRAGMA table_info({tbl})'))
            print(f'\n=== {tbl} ===')
            for row in result:
                print(f'  {row[1]:20} {row[2]}')
asyncio.run(check())
"
```

---

## Kiến Thức Áp Dụng Trong Phase Này

| Kiến thức | Áp dụng cụ thể |
|----------|---------------|
| `DeclarativeBase` | Base class cho tất cả ORM models |
| `Mapped[T]` | Type-safe column definition |
| `mapped_column()` | Column với constraints |
| `relationship()` | ORM join giữa 2 bảng |
| `alembic autogenerate` | Detect thay đổi schema tự động |
| `render_as_batch` | Fix SQLite ALTER TABLE limitation |
| `async_engine_from_config` | Alembic dùng async engine thay vì sync |

---

## Điểm Rút Ra

- `alembic init alembic` chỉ tạo bộ khung — phải sửa cả `alembic.ini` (URL) lẫn `env.py` (async engine) mới chạy được
- Model phải được import vào `__init__.py` trước khi `alembic revision --autogenerate` chạy, nếu không Alembic sẽ không detect được bảng
- `render_as_batch=True` là bắt buộc khi dùng SQLite — thiếu cái này sẽ bể migration ngay lần đầu thêm/đổi cột

---

## Lỗi Gặp Phải

| # | Lỗi | Fix | Entry trong error-log |
|---|-----|-----|-----------------------|
| — | Không gặp lỗi trong phase này | — | — |
