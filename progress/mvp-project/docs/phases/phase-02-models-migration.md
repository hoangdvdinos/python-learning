# Phase 2 — ORM Models & Migration

## Trạng Thái

- [ ] Đang làm
- [ ] Hoàn thành

**Bắt đầu:** ___________  
**Kết thúc:** ___________

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

---

### Bước 2.2 — Category Model

**Làm gì:** Viết `app/models/category.py`.

**Tại sao `Mapped[str | None]` cho `icon` và `color`?**
- `Mapped[str]` → NOT NULL trong DB
- `Mapped[str | None]` → nullable, client có thể không gửi
- SQLAlchemy 2.0 dùng type annotation thay vì `Column(nullable=True)` cũ

**Kiến thức áp dụng:** Khối 4 — Type hints, Khối 11 — Mapped[T]

---

### Bước 2.3 — Transaction Model

**Làm gì:** Viết `app/models/transaction.py` với ForeignKey tới categories.

**Tại sao cần `relationship("Category", lazy="selectin")`?**
- Khi query Transaction, cần hiển thị `category_name` trong response
- `lazy="selectin"` → SQLAlchemy tự JOIN, không cần viết JOIN thủ công
- Tránh N+1 problem: 10 transactions → 1 query, không phải 11 queries

**Kiến thức áp dụng:** Khối 11 — relationship, selectinload

---

### Bước 2.4 — `__init__.py` cho models

**Làm gì:** Import tất cả models vào `app/models/__init__.py`.

**Tại sao cần làm bước này?**
Alembic scan `target_metadata` để biết schema.
Nếu model chưa được import → Alembic không biết model tồn tại → không generate migration.
File này là "registration point" — phải import trước khi Alembic chạy.

---

### Bước 2.5 — Cấu hình Alembic

**Làm gì:**
```bash
alembic init alembic
```
Sau đó sửa `alembic/env.py` để dùng async engine.

**Tại sao `render_as_batch=True`?**
SQLite không support `ALTER TABLE ... ADD COLUMN` / `DROP COLUMN`.
`render_as_batch=True` khiến Alembic dùng cách khác: tạo bảng temp → copy data → drop bảng cũ → rename.
Nếu không bật → migration sẽ fail khi thay đổi schema trên SQLite.

**Kiến thức áp dụng:** Khối 11 — Alembic async config

---

### Bước 2.6 — Tạo và chạy migration

**Làm gì:**
```bash
alembic revision --autogenerate -m "init categories and transactions"
alembic upgrade head
```

**Verify:**
```bash
uv run python -c "
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
async def check():
    engine = create_async_engine('sqlite+aiosqlite:///finance.db')
    async with engine.connect() as conn:
        result = await conn.execute(__import__('sqlalchemy').text('SELECT name FROM sqlite_master WHERE type=table'))
        print([r[0] for r in result])
asyncio.run(check())
"
# Mong đợi: ['categories', 'transactions', 'alembic_version']
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
