# FastAPI MVP Project Ideas

> Mục đích: Practice toàn bộ kiến thức Khối 1–11
> Tiêu chí chọn: Đủ phức tạp để dùng đúng tool, đủ đơn giản để hoàn thành trong 2–3 ngày

---

## Kiến Thức Cần Cover

| Khối | Nội dung |
|------|----------|
| 1–6 | Python cơ bản, OOP, Exception, File |
| 7–8 | Type Hints, Async, Pydantic v2 |
| 9 | FastAPI Routing, Path/Query/Body |
| 10 | Form, Headers, Custom Exception, APIRouter, Middleware, CORS |
| 11 | Dependency Injection, SQLAlchemy 2.0, CRUD, Alembic |

---

## Chủ Đề 1 — Personal Finance Tracker

**Mô tả:** API quản lý thu chi cá nhân. Người dùng tạo tài khoản, ghi lại giao dịch (income/expense), xem báo cáo tổng hợp theo tháng.

**Tính năng MVP:**
- CRUD Categories (Ăn uống, Di chuyển, Lương...)
- CRUD Transactions (amount, type, category, note, date)
- Thống kê: tổng thu / tổng chi / balance theo tháng
- Filter: theo category, theo date range, theo type

**Vì sao phù hợp:**
- 2 entity có quan hệ (Category → Transaction) → practice SQLAlchemy relationship
- Endpoint thống kê → practice SQL aggregation (`func.sum`, `group_by`)
- Filter phức tạp → practice query builder
- Soft delete (transaction không xóa thật)

**Độ phức tạp:** ⭐⭐⭐ Trung bình

---

## Chủ Đề 2 — Task Manager (To-do API)

**Mô tả:** API quản lý công việc kiểu Trello đơn giản. Có Projects, mỗi project có nhiều Tasks, task có priority và status.

**Tính năng MVP:**
- CRUD Projects
- CRUD Tasks thuộc Project (title, description, priority, status, due_date)
- Filter tasks: theo status, priority, overdue
- Bulk update: đánh dấu nhiều task done cùng lúc
- Middleware log request time

**Vì sao phù hợp:**
- Project → Task: quan hệ 1-nhiều với cascade delete
- Bulk operation → practice SQLAlchemy `update()` statement
- Status enum → practice Python Enum + SQLAlchemy
- Overdue filter → practice so sánh datetime trong query

**Độ phức tạp:** ⭐⭐⭐ Trung bình

---

## Chủ Đề 3 — URL Shortener

**Mô tả:** API rút gọn URL kiểu bit.ly. Tạo short code, redirect, đếm số lần click, xem analytics.

**Tính năng MVP:**
- Tạo short URL từ long URL (sinh code ngẫu nhiên hoặc custom)
- Redirect: GET `/{code}` → 301/302 đến URL gốc
- Click tracking: đếm tổng click, lưu IP + timestamp
- Analytics: top 10 URL được click nhiều nhất, click theo ngày
- Expire: short URL hết hạn sau N ngày

**Vì sao phù hợp:**
- `RedirectResponse` → practice trả response không phải JSON
- Background Task: ghi click log sau khi redirect (không block người dùng)
- Aggregation query phức tạp hơn → practice `group_by`, `order_by`, `limit`
- Unique constraint handling → practice SQLAlchemy exception

**Độ phức tạp:** ⭐⭐⭐⭐ Trung bình-Cao

---

## Chủ Đề 4 — Product Catalog API

**Mô tả:** API catalog sản phẩm cho e-commerce nhỏ. Có Categories, Products, và tính năng tìm kiếm/lọc.

**Tính năng MVP:**
- CRUD Categories (có hierarchy: category cha/con)
- CRUD Products (name, price, stock, images list, category)
- Search: full-text search theo name/description
- Filter: price range, category, in-stock only
- Pagination chuẩn (page/limit + metadata)
- Upload ảnh sản phẩm (lưu local hoặc trả base64)

**Vì sao phù hợp:**
- Self-referencing relationship (Category parent/child) → nâng cao hơn
- `File Upload` + validation type/size → practice khối 10
- Search với `ilike` → practice query linh hoạt
- JSON column (images list) → practice SQLAlchemy JSON type

**Độ phức tạp:** ⭐⭐⭐⭐ Trung bình-Cao

---

## Chủ Đề 5 — Expense Splitter (Chia tiền nhóm)

**Mô tả:** API chia tiền cho nhóm bạn đi du lịch / ăn uống. Tạo group, thêm member, ghi chi phí, tính toán ai nợ ai bao nhiêu.

**Tính năng MVP:**
- CRUD Groups + Members
- CRUD Expenses (amount, paid_by, split_among)
- Tính toán: settle up — ai cần trả cho ai, bao nhiêu
- Lịch sử thanh toán

**Vì sao phù hợp:**
- Many-to-many relationship (Expense ↔ Member) → practice association table
- Business logic phức tạp (debt calculation) → tách ra service layer riêng
- Custom validator Pydantic: tổng split phải bằng 100%
- Pure Python algorithm → practice OOP + data structures

**Độ phức tạp:** ⭐⭐⭐⭐⭐ Cao

---

## Bảng So Sánh

| # | Chủ đề | Độ phức tạp | Thời gian ước tính | Điểm nổi bật |
|---|--------|------------|-------------------|--------------|
| 1 | Personal Finance Tracker | ⭐⭐⭐ | 1.5–2 ngày | Aggregation, soft delete |
| 2 | Task Manager | ⭐⭐⭐ | 1.5–2 ngày | Enum, bulk update, overdue |
| 3 | URL Shortener | ⭐⭐⭐⭐ | 2–3 ngày | Redirect, Background Task, analytics |
| 4 | Product Catalog | ⭐⭐⭐⭐ | 2–3 ngày | File upload, search, self-ref relation |
| 5 | Expense Splitter | ⭐⭐⭐⭐⭐ | 3–4 ngày | M2M, business logic phức tạp |

---

## Gợi Ý Chọn

- **Muốn chắc chắn hoàn thành nhanh** → Chủ đề 1 hoặc 2
- **Muốn practice nhiều tính năng FastAPI nhất** → Chủ đề 3 (có redirect, background task, analytics)
- **Muốn gần với dự án thực tế** → Chủ đề 4 (e-commerce là domain quen thuộc)
- **Muốn thử thách** → Chủ đề 5

---

## Tech Stack Chung (Tất cả chủ đề)

```
Runtime    : Python 3.12+
Framework  : FastAPI 0.136+
ORM        : SQLAlchemy 2.0 async
Database   : SQLite (dev, không cần cài PostgreSQL)
Migration  : Alembic
Validation : Pydantic v2
Server     : Uvicorn
Package    : uv
```

> Dùng SQLite để không mất thời gian setup PostgreSQL — SQLAlchemy code giống nhau, chỉ đổi URL là chạy được PostgreSQL.
