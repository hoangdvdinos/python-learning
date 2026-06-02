# Personal Finance Tracker

REST API quản lý thu chi cá nhân, xây dựng bằng FastAPI + SQLAlchemy + SQLite.

## Mục đích

Dự án **practice** để áp dụng kiến thức FastAPI vào một project thực tế — không phải production.

## Tính năng

- CRUD **Category** — quản lý danh mục thu/chi (ăn uống, lương, điện nước...)
- CRUD **Transaction** — ghi lại giao dịch tiền vào/ra theo danh mục
- **Report API** — tổng hợp thu chi theo tháng, theo danh mục
- Soft delete — không xóa cứng dữ liệu
- Validation đầu vào qua Pydantic

## Không có

- Authentication / Authorization
- Frontend
- Multi-user
- Deployment / Docker

## Tech Stack

| Thành phần | Lựa chọn |
|-----------|----------|
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 async |
| Database | SQLite (aiosqlite) |
| Migration | Alembic |
| Validation | Pydantic v2 |
| Config | pydantic-settings |
| Package manager | uv |

## Chạy project

```bash
uv run uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs
