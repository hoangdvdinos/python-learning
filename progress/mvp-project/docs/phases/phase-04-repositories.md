# Phase 4 — Repositories

## Trạng Thái

- [ ] Đang làm
- [x] Hoàn thành

**Bắt đầu:** 2026-06-02  
**Kết thúc:** 2026-06-02

---

## Tổng Quan Phase Này

**Làm gì:** Viết 3 repository classes chứa toàn bộ database logic.

**Đây là phase quan trọng nhất** — business logic nằm ở đây:
- Soft delete check (category có transactions không?)
- Auto-derive transaction type từ category
- Dynamic filter builder cho list endpoints
- Aggregate queries cho reports

**Kết quả mong đợi:** Import thành công, không lỗi:
```bash
uv run python -c "from app.repositories import CategoryRepository, TransactionRepository, ReportRepository; print('OK')"
```

---

## Các Bước Thực Hiện

### Bước 4.1 — CategoryRepository

**Làm gì:** Viết `app/repositories/category_repo.py`.

**Giải thích `soft_delete` check:**
```python
stmt = select(func.count(Transaction.id)).where(
    Transaction.category_id == category_id,
    Transaction.is_deleted == False,
)
count = await self.session.scalar(stmt)
if count and count > 0:
    raise BusinessException(f"Cannot delete category with {count} active transaction(s).")
```
**Tại sao?** Nếu cho phép xóa category đang dùng → transactions mồ côi (orphan),
báo cáo sẽ không group được. Business rule: phải xóa transactions trước.

**Giải thích `session.flush()` thay vì `session.commit()`:**
- `flush()` → ghi xuống DB trong cùng transaction, chưa commit
- `commit()` được gọi ở tầng trên (dependency `get_db` trong `database.py`)
- Repository không được tự commit — tầng nào chịu trách nhiệm session, tầng đó commit

**Code thực tế:**
```python
class CategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[Category]: ...
    async def get_by_id(self, category_id: int) -> Category: ...  # raise NotFoundException nếu không tìm thấy
    async def create(self, data: CategoryCreate) -> Category: ...
    async def update(self, category_id: int, data: CategoryUpdate) -> Category: ...
    async def delete(self, category_id: int) -> None: ...  # soft delete với guard
```

**Kiến thức áp dụng:** Khối 11 — async SQLAlchemy, Khối 7 — CRUD

**Lệnh:** *(không có lệnh shell — chỉ tạo file)*

---

### Bước 4.2 — TransactionRepository

**Làm gì:** Viết `app/repositories/transaction_repo.py`.

**Giải thích dynamic filter builder:**
```python
filters = [Transaction.is_deleted == False]
if type:
    filters.append(Transaction.type == type)
if category_id:
    filters.append(Transaction.category_id == category_id)
if date_from:
    filters.append(Transaction.transaction_date >= date_from)
if date_to:
    filters.append(Transaction.transaction_date <= date_to)

stmt = select(Transaction).where(*filters)
```
**Tại sao không dùng `if/else` riêng?** Sẽ phải viết `2^n` combinations cho n filters.
List accumulation cho phép combine tùy ý — thêm filter mới chỉ cần thêm 1 dòng `append`.

**Giải thích `selectinload` cho pagination:**
```python
stmt = (
    select(Transaction)
    .where(*filters)
    .options(selectinload(Transaction.category))
    .order_by(Transaction.transaction_date.desc())
    .offset((page - 1) * size)
    .limit(size)
)
```
`selectinload` emit 2 queries thay vì JOIN:
1. `SELECT * FROM transactions WHERE ... LIMIT 20`
2. `SELECT * FROM categories WHERE id IN (1, 2, 3, ...)`

So với JOIN: nếu category có nhiều transactions, JOIN sẽ duplicate data category ở mỗi row.

**Giải thích auto-derive type:**
```python
async def create(self, data: TransactionCreate) -> Transaction:
    category = await self._category_repo.get_by_id(data.category_id)
    transaction = Transaction(**data.model_dump(), type=category.type)
```
Client không gửi `type` — repository tự lấy từ category để đảm bảo consistency.
Update cũng re-derive nếu `category_id` thay đổi.

**Kiến thức áp dụng:** Khối 11 — selectinload, pagination

**Lệnh:** *(không có lệnh shell — chỉ tạo file)*

---

### Bước 4.3 — ReportRepository

**Làm gì:** Viết `app/repositories/report_repo.py` với 3 aggregate queries.

**Giải thích `case()` trong summary và monthly:**
```python
income_col = func.sum(
    case((Transaction.type == "income", Transaction.amount), else_=0)
)
expense_col = func.sum(
    case((Transaction.type == "expense", Transaction.amount), else_=0)
)
```
**Tại sao không query 2 lần?** Một query GROUP BY month, dùng CASE để split income/expense
trong cùng row → 12 rows cho 12 tháng, thay vì 24 rows (2 type × 12 tháng).

**Giải thích `extract("year", Transaction.transaction_date)`:**
SQLAlchemy cross-DB way để lấy year/month từ DATE column.
Tương đương `EXTRACT(YEAR FROM transaction_date)` trong SQL thuần.

**3 endpoints report:**
| Method | Query | Mô tả |
|--------|-------|--------|
| `get_summary()` | SUM với CASE | Tổng income/expense/balance toàn thời gian |
| `get_monthly()` | GROUP BY year, month | Breakdown theo từng tháng |
| `get_by_category()` | JOIN + GROUP BY category | Breakdown theo danh mục |

**Kiến thức áp dụng:** Khối 11 — func.sum, group_by, extract

**Lệnh:** *(không có lệnh shell — chỉ tạo file)*

---

### Bước 4.4 — `__init__.py` cho repositories

**Làm gì:** Export tất cả repos từ `app/repositories/__init__.py`.

**Verify:**
```bash
uv run python -c "
from app.repositories import CategoryRepository, TransactionRepository, ReportRepository
print('OK:', CategoryRepository, TransactionRepository, ReportRepository)
"
# Kết quả: OK: <class ...> <class ...> <class ...>
```

---

## Kiến Thức Áp Dụng Trong Phase Này

| Kiến thức | Áp dụng cụ thể |
|----------|---------------|
| `select(Model)` | SQLAlchemy 2.0 query style |
| `session.execute()` + `.scalars()` | Async query, lấy list |
| `session.scalar()` | Lấy single value (count) |
| `scalar_one_or_none()` | Lấy 1 row, trả None nếu không có |
| `selectinload()` | Eager load relationship, tránh N+1 |
| `session.flush()` | Ghi xuống DB mà chưa commit |
| `func.sum()`, `func.count()` | SQL aggregate |
| `group_by()`, `extract()` | Grouping và date extraction |
| `case()` | Conditional aggregate (CASE WHEN) |
| `model_dump(exclude_unset=True)` | PATCH — chỉ update field client gửi |

---

## Điểm Rút Ra

- Repository không được tự `commit()` — trách nhiệm commit thuộc về dependency `get_db` ở tầng trên; repo chỉ `flush()`
- Dynamic filter dùng list `filters = [...]` + `append()` — thêm filter mới không cần sửa logic cũ
- `scalar_one_or_none()` trả `None` thay vì raise exception — phải tự raise `NotFoundException` sau đó

---

## Lỗi Gặp Phải

| # | Lỗi | Fix | Entry trong error-log |
|---|-----|-----|-----------------------|
| — | Không gặp lỗi trong phase này | — | — |
