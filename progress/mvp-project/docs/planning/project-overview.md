# Project Overview — Personal Finance Tracker

## Mục Tiêu

Xây dựng một REST API quản lý thu chi cá nhân.
Mục đích chính là **practice** kiến thức từ Khối 1–11, không phải production.

## Scope (Làm)

- CRUD cho **Category** (danh mục thu/chi)
- CRUD cho **Transaction** (giao dịch)
- **Report API**: tổng hợp, theo tháng, theo danh mục
- Soft delete (không xóa cứng)
- Validation đầu vào qua Pydantic

## Out of Scope (Không làm)

- Authentication / Authorization
- Multi-user / tenant
- Frontend
- Deployment / Docker

## Knowledge Coverage

| Khối | Áp dụng vào đâu |
|------|----------------|
| Khối 4 — Type Hints | Tất cả function signatures |
| Khối 5 — Pydantic | Schemas (request/response validation) |
| Khối 6 — FastAPI Cơ Bản | Router, path/query params |
| Khối 7 — CRUD | Repository pattern |
| Khối 8 — Validation | Field validators trong schema |
| Khối 9 — Routing | APIRouter, prefix, tags |
| Khối 10 — Request/Response Nâng Cao | Exception handlers, middleware |
| Khối 11 — DI & Database | SQLAlchemy, Alembic, Depends |

## Tech Stack

| Thành phần | Lựa chọn | Lý do |
|-----------|----------|-------|
| Framework | FastAPI | Đang học |
| ORM | SQLAlchemy 2.0 async | Khối 11 |
| Database | SQLite (aiosqlite) | Đơn giản cho dev |
| Migration | Alembic | Chuẩn production |
| Validation | Pydantic v2 | Khối 5 |
| Config | pydantic-settings | Best practice |
| Package manager | uv | Nhanh hơn pip |

## Thư Mục Project

```
finance-tracker/
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── routers/
│   └── main.py
├── alembic/
├── .env
└── pyproject.toml
```
