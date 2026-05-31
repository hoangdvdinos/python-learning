# MVP Project 01 — Personal Finance Tracker

> **Mục đích:** Practice Khối 1–11 trên một project thực tế hoàn chỉnh
> **Thời gian ước tính:** 1.5–2 ngày
> **Database:** SQLite (dev) — đổi URL là chạy PostgreSQL production

---

## 1. Tổng Quan Hệ Thống

### 1.1 Mô tả

API quản lý thu chi cá nhân. Người dùng tạo danh mục (categories), ghi lại các giao dịch (transactions), và xem báo cáo tổng hợp theo tháng.

### 1.2 Entities

```
Category ──< Transaction
(1)           (nhiều)
```

- **Category**: Nhóm phân loại (Ăn uống, Di chuyển, Lương, Nhà ở...)
- **Transaction**: Mỗi khoản thu hoặc chi, thuộc về 1 Category

### 1.3 Kiến thức được dùng

| Khối | Áp dụng vào đâu |
|------|-----------------|
| Type Hints + Pydantic | Schemas request/response |
| FastAPI Routing | Path params, Query params, Body |
| APIRouter | Tách `categories` và `transactions` module |
| Custom Exception | `NotFoundException`, `ValidationException` |
| Middleware | Log request + timing |
| CORS | Cho phép frontend gọi API |
| Depends() | DB session, pagination params |
| SQLAlchemy 2.0 | ORM models + async CRUD |
| Alembic | Migration tạo bảng |
| Aggregation SQL | Báo cáo tổng thu/chi theo tháng |
| Soft delete | Transaction không xóa thật |

---

## 2. Cấu Trúc Thư Mục

```
finance-tracker/
├── main.py                         ← entry point
├── pyproject.toml
├── .env
├── .env.example
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/
└── app/
    ├── __init__.py
    ├── core/
    │   ├── __init__.py
    │   ├── config.py               ← Pydantic Settings
    │   ├── database.py             ← engine, session, get_db
    │   └── exceptions.py           ← AppException, NotFoundException
    ├── models/
    │   ├── __init__.py
    │   ├── base.py                 ← DeclarativeBase, TimestampMixin
    │   ├── category.py
    │   └── transaction.py
    ├── schemas/
    │   ├── __init__.py
    │   ├── category.py
    │   ├── transaction.py
    │   └── report.py               ← schema cho response báo cáo
    ├── repositories/
    │   ├── __init__.py
    │   ├── category_repo.py
    │   └── transaction_repo.py
    └── routers/
        ├── __init__.py
        ├── categories.py
        ├── transactions.py
        └── reports.py
```

---

## 3. Database Schema

### 3.1 Bảng `categories`

| Column | Type | Constraint | Mô tả |
|--------|------|-----------|-------|
| `id` | INTEGER | PK, autoincrement | |
| `name` | VARCHAR(100) | NOT NULL, UNIQUE | Tên danh mục |
| `type` | VARCHAR(10) | NOT NULL | `income` hoặc `expense` |
| `icon` | VARCHAR(50) | NULL | Emoji hoặc icon code |
| `color` | VARCHAR(7) | NULL | Hex color `#FF5733` |
| `is_active` | BOOLEAN | NOT NULL, default=true | Soft delete |
| `created_at` | DATETIME | NOT NULL | |
| `updated_at` | DATETIME | NOT NULL | |

### 3.2 Bảng `transactions`

| Column | Type | Constraint | Mô tả |
|--------|------|-----------|-------|
| `id` | INTEGER | PK, autoincrement | |
| `category_id` | INTEGER | FK → categories.id, NOT NULL | |
| `amount` | NUMERIC(12,2) | NOT NULL, > 0 | Số tiền (luôn dương) |
| `type` | VARCHAR(10) | NOT NULL | `income` hoặc `expense` |
| `note` | TEXT | NULL | Ghi chú |
| `transaction_date` | DATE | NOT NULL | Ngày giao dịch (do user nhập) |
| `is_deleted` | BOOLEAN | NOT NULL, default=false | Soft delete |
| `created_at` | DATETIME | NOT NULL | |
| `updated_at` | DATETIME | NOT NULL | |

> **Lý do `type` lưu cả ở transaction:** Category có type mặc định, nhưng transaction ghi lại type tại thời điểm tạo — tránh báo cáo sai khi category bị thay đổi sau.

---

## 4. API Endpoints

### 4.1 Categories

| Method | Path | Mô tả | Status |
|--------|------|-------|--------|
| `GET` | `/categories` | Danh sách categories | 200 |
| `POST` | `/categories` | Tạo category mới | 201 |
| `GET` | `/categories/{id}` | Chi tiết category | 200 / 404 |
| `PATCH` | `/categories/{id}` | Cập nhật category | 200 / 404 |
| `DELETE` | `/categories/{id}` | Soft delete category | 204 / 404 |

**Query params cho `GET /categories`:**
- `type`: `income` | `expense` | không truyền = tất cả
- `is_active`: `true` | `false` | không truyền = chỉ active

### 4.2 Transactions

| Method | Path | Mô tả | Status |
|--------|------|-------|--------|
| `GET` | `/transactions` | Danh sách transactions (có filter + phân trang) | 200 |
| `POST` | `/transactions` | Tạo transaction mới | 201 |
| `GET` | `/transactions/{id}` | Chi tiết transaction | 200 / 404 |
| `PATCH` | `/transactions/{id}` | Cập nhật transaction | 200 / 404 |
| `DELETE` | `/transactions/{id}` | Soft delete (is_deleted=true) | 204 / 404 |

**Query params cho `GET /transactions`:**
- `page`: số trang (default=1)
- `limit`: số item mỗi trang (default=20, max=100)
- `type`: `income` | `expense`
- `category_id`: lọc theo category
- `from_date`: `YYYY-MM-DD`
- `to_date`: `YYYY-MM-DD`

### 4.3 Reports

| Method | Path | Mô tả | Status |
|--------|------|-------|--------|
| `GET` | `/reports/summary` | Tổng thu/chi/balance trong khoảng thời gian | 200 |
| `GET` | `/reports/monthly` | Thu/chi theo từng tháng (12 tháng gần nhất) | 200 |
| `GET` | `/reports/by-category` | Thu/chi nhóm theo category trong khoảng thời gian | 200 |

**Query params cho `/reports/summary` và `/reports/by-category`:**
- `from_date`: bắt buộc, `YYYY-MM-DD`
- `to_date`: bắt buộc, `YYYY-MM-DD`

---

## 5. Request / Response Schema

### 5.1 Category Schemas

```python
# POST /categories — Request Body
{
    "name": "Ăn uống",
    "type": "expense",       # "income" | "expense"
    "icon": "🍜",            # optional
    "color": "#FF5733"       # optional
}

# Response (GET, POST, PATCH)
{
    "id": 1,
    "name": "Ăn uống",
    "type": "expense",
    "icon": "🍜",
    "color": "#FF5733",
    "is_active": true,
    "created_at": "2026-05-31T08:00:00Z",
    "updated_at": "2026-05-31T08:00:00Z"
}
```

### 5.2 Transaction Schemas

```python
# POST /transactions — Request Body
{
    "category_id": 1,
    "amount": 85000,
    "note": "Bún bò Huế buổi trưa",
    "transaction_date": "2026-05-31"
}
# type được tự động lấy từ category.type

# Response
{
    "id": 10,
    "category_id": 1,
    "category_name": "Ăn uống",     # join từ category
    "amount": "85000.00",
    "type": "expense",
    "note": "Bún bò Huế buổi trưa",
    "transaction_date": "2026-05-31",
    "created_at": "2026-05-31T12:30:00Z",
    "updated_at": "2026-05-31T12:30:00Z"
}

# GET /transactions — Response (paginated)
{
    "data": [ ...transactions... ],
    "total": 87,
    "page": 1,
    "limit": 20
}
```

### 5.3 Report Schemas

```python
# GET /reports/summary?from_date=2026-05-01&to_date=2026-05-31
{
    "from_date": "2026-05-01",
    "to_date": "2026-05-31",
    "total_income": "15000000.00",
    "total_expense": "8750000.00",
    "balance": "6250000.00"
}

# GET /reports/monthly
{
    "data": [
        {"year": 2026, "month": 5, "income": "15000000.00", "expense": "8750000.00", "balance": "6250000.00"},
        {"year": 2026, "month": 4, "income": "14500000.00", "expense": "9200000.00", "balance": "5300000.00"}
    ]
}

# GET /reports/by-category?from_date=2026-05-01&to_date=2026-05-31
{
    "from_date": "2026-05-01",
    "to_date": "2026-05-31",
    "data": [
        {"category_id": 1, "category_name": "Ăn uống", "type": "expense", "total": "2500000.00", "count": 30},
        {"category_id": 2, "category_name": "Lương",   "type": "income",  "total": "15000000.00", "count": 1}
    ]
}
```

---

## 6. Kế Hoạch Triển Khai

### Phase 1 — Setup (30 phút)

```
[ ] 1.1  Tạo project với uv: uv init finance-tracker
[ ] 1.2  Cài dependencies
[ ] 1.3  Tạo cấu trúc thư mục
[ ] 1.4  Cấu hình .env + config.py
[ ] 1.5  Cấu hình database.py (engine + session)
[ ] 1.6  Khởi tạo Alembic
```

**Dependencies:**
```bash
uv add fastapi uvicorn[standard] sqlalchemy[asyncio] aiosqlite alembic pydantic-settings
uv add --dev httpx pytest ruff
```

### Phase 2 — Models + Migration (30 phút)

```
[ ] 2.1  Tạo base.py — DeclarativeBase + TimestampMixin
[ ] 2.2  Tạo models/category.py
[ ] 2.3  Tạo models/transaction.py
[ ] 2.4  Cấu hình alembic/env.py
[ ] 2.5  Chạy: alembic revision --autogenerate -m "init"
[ ] 2.6  Chạy: alembic upgrade head
[ ] 2.7  Kiểm tra DB bằng DB browser hoặc sqlite3 CLI
```

### Phase 3 — Schemas + Exceptions (30 phút)

```
[ ] 3.1  Tạo schemas/category.py
         — CategoryCreate, CategoryUpdate, CategoryResponse
[ ] 3.2  Tạo schemas/transaction.py
         — TransactionCreate, TransactionUpdate, TransactionResponse, TransactionListResponse
[ ] 3.3  Tạo schemas/report.py
         — SummaryResponse, MonthlyItem, MonthlyResponse, ByCategoryItem, ByCategoryResponse
[ ] 3.4  Tạo core/exceptions.py
         — AppException, NotFoundException, BusinessException
[ ] 3.5  Đăng ký exception handlers trong main.py
```

### Phase 4 — Repositories (45 phút)

```
[ ] 4.1  Tạo repositories/category_repo.py
         — get_by_id, list, create, update, soft_delete
[ ] 4.2  Tạo repositories/transaction_repo.py
         — get_by_id, list (filter + paginate), create, update, soft_delete
[ ] 4.3  Tạo repositories/report_repo.py
         — get_summary, get_monthly, get_by_category
         (dùng func.sum, func.count, group_by, extract)
```

### Phase 5 — Routers + main.py (45 phút)

```
[ ] 5.1  Tạo routers/categories.py — 5 endpoints
[ ] 5.2  Tạo routers/transactions.py — 5 endpoints
[ ] 5.3  Tạo routers/reports.py — 3 endpoints
[ ] 5.4  Tạo main.py: app, lifespan, middleware, CORS, include routers
[ ] 5.5  Chạy server: uvicorn main:app --reload
[ ] 5.6  Test toàn bộ endpoint trên Swagger /docs
```

### Phase 6 — Polish (30 phút) — Tùy chọn

```
[ ] 6.1  Seed data: thêm categories + transactions mẫu
[ ] 6.2  Validate: không cho xóa category còn transaction
[ ] 6.3  Health check endpoint: GET /health
[ ] 6.4  README.md với hướng dẫn chạy
```

---

## 7. Implementation Notes

### 7.1 Logic tự động lấy `type` từ Category

```python
# Khi tạo transaction, không truyền type vào body
# Repository tự query category để lấy type

async def create(self, db: AsyncSession, data: TransactionCreate) -> Transaction:
    category = await db.get(Category, data.category_id)
    if category is None:
        raise NotFoundException("Category", data.category_id)

    transaction = Transaction(
        **data.model_dump(),
        type=category.type,   # ← lấy từ category
    )
    db.add(transaction)
    await db.flush()
    await db.refresh(transaction)
    return transaction
```

### 7.2 Query báo cáo — dùng SQLAlchemy aggregation

```python
from sqlalchemy import select, func, extract, and_

# Summary
async def get_summary(self, db: AsyncSession, from_date, to_date):
    query = (
        select(
            Transaction.type,
            func.sum(Transaction.amount).label("total"),
        )
        .where(and_(
            Transaction.is_deleted == False,
            Transaction.transaction_date >= from_date,
            Transaction.transaction_date <= to_date,
        ))
        .group_by(Transaction.type)
    )
    rows = (await db.execute(query)).all()
    # Xử lý rows → SummaryResponse

# Monthly — group by year + month
query = (
    select(
        extract("year",  Transaction.transaction_date).label("year"),
        extract("month", Transaction.transaction_date).label("month"),
        Transaction.type,
        func.sum(Transaction.amount).label("total"),
    )
    .where(Transaction.is_deleted == False)
    .group_by("year", "month", Transaction.type)
    .order_by("year", "month")
)
```

### 7.3 Filter transactions với query builder

```python
async def list(self, db, page, limit, type=None, category_id=None, from_date=None, to_date=None):
    conditions = [Transaction.is_deleted == False]

    if type is not None:
        conditions.append(Transaction.type == type)
    if category_id is not None:
        conditions.append(Transaction.category_id == category_id)
    if from_date is not None:
        conditions.append(Transaction.transaction_date >= from_date)
    if to_date is not None:
        conditions.append(Transaction.transaction_date <= to_date)

    base = select(Transaction).where(and_(*conditions))
    total = (await db.execute(select(func.count()).select_from(base.subquery()))).scalar_one()
    rows  = (await db.execute(
        base.order_by(Transaction.transaction_date.desc())
            .offset((page - 1) * limit)
            .limit(limit)
    )).scalars().all()

    return rows, total
```

### 7.4 Response có `category_name` — join query

```python
from sqlalchemy.orm import selectinload

# Option 1: selectinload (khuyến nghị)
async def get_by_id(self, db, transaction_id):
    query = (
        select(Transaction)
        .options(selectinload(Transaction.category))
        .where(Transaction.id == transaction_id, Transaction.is_deleted == False)
    )
    return (await db.execute(query)).scalar_one_or_none()

# Schema đọc từ ORM
class TransactionResponse(BaseModel):
    id: int
    category_id: int
    category_name: str    # đọc từ transaction.category.name
    amount: Decimal
    ...

    @model_validator(mode="before")
    @classmethod
    def extract_category_name(cls, data):
        if hasattr(data, "category") and data.category:
            data.__dict__["category_name"] = data.category.name
        return data
```

---

## 8. Seed Data Mẫu

```python
# seed.py — chạy 1 lần để có data test
CATEGORIES = [
    {"name": "Lương",       "type": "income",  "icon": "💼", "color": "#4CAF50"},
    {"name": "Thưởng",      "type": "income",  "icon": "🎁", "color": "#8BC34A"},
    {"name": "Đầu tư",      "type": "income",  "icon": "📈", "color": "#009688"},
    {"name": "Ăn uống",     "type": "expense", "icon": "🍜", "color": "#FF5722"},
    {"name": "Di chuyển",   "type": "expense", "icon": "🚗", "color": "#FF9800"},
    {"name": "Nhà ở",       "type": "expense", "icon": "🏠", "color": "#795548"},
    {"name": "Mua sắm",     "type": "expense", "icon": "🛍️", "color": "#E91E63"},
    {"name": "Giải trí",    "type": "expense", "icon": "🎮", "color": "#9C27B0"},
    {"name": "Sức khỏe",    "type": "expense", "icon": "💊", "color": "#F44336"},
    {"name": "Học tập",     "type": "expense", "icon": "📚", "color": "#2196F3"},
]
```

---

## 9. Checklist Tự Kiểm Tra

### Functional
```
[ ] GET /categories trả đúng danh sách, filter by type hoạt động
[ ] POST /categories validate required fields, trả 201
[ ] PATCH /categories/{id} chỉ update field được truyền
[ ] DELETE /categories/{id} soft delete → GET không còn thấy
[ ] POST /transactions tự gán type từ category
[ ] GET /transactions filter by type + category_id + date range
[ ] GET /transactions phân trang đúng (total, page, limit)
[ ] GET /reports/summary tính đúng income/expense/balance
[ ] GET /reports/monthly nhóm đúng theo tháng
[ ] GET /reports/by-category nhóm đúng theo category
```

### Error Handling
```
[ ] GET /categories/999 → 404 với message rõ ràng
[ ] POST /transactions với category_id không tồn tại → 404
[ ] POST /transactions với amount = 0 → 422
[ ] POST /transactions thiếu required field → 422 với field name
```

### Code Quality
```
[ ] Mỗi router file không có business logic (chỉ gọi repo)
[ ] Mỗi repo method chỉ làm 1 việc
[ ] Exception handler toàn cục hoạt động (không để lộ stack trace)
[ ] Type hints đầy đủ ở mọi function signature
```
