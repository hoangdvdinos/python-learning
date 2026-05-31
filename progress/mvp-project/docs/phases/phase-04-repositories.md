# Phase 4 — Repositories

## Trạng Thái

- [ ] Đang làm
- [ ] Hoàn thành

**Bắt đầu:** ___________  
**Kết thúc:** ___________

---

## Tổng Quan Phase Này

**Làm gì:** Viết 3 repository classes chứa toàn bộ database logic.

**Đây là phase quan trọng nhất** — business logic nằm ở đây:
- Soft delete check (category có transactions không?)
- Auto-derive transaction type từ category
- Dynamic filter builder cho list endpoints
- Aggregate queries cho reports

**Kết quả mong đợi:** Test trực tiếp từng repo function trong Python shell.

---

## Các Bước Thực Hiện

### Bước 4.1 — CategoryRepository

**Làm gì:** Viết `app/repositories/category_repo.py`.

**Giải thích `soft_delete` check:**
```python
# Kiểm tra có transaction active không
stmt = select(func.count(Transaction.id)).where(
    Transaction.category_id == category_id,
    Transaction.is_deleted == False
)
count = await session.scalar(stmt)
if count > 0:
    raise BusinessException(f"Cannot delete category with {count} active transactions")
```
**Tại sao làm vậy?** Nếu cho phép xóa category đang dùng → transactions mồ côi (orphan),
báo cáo sẽ không group được. Business rule: phải xóa/move transactions trước.

**Kiến thức áp dụng:** Khối 11 — async SQLAlchemy, Khối 7 — CRUD

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
stmt = select(Transaction).where(*filters)
```
**Tại sao không dùng `if/else` riêng?** Sẽ phải viết `2^n` combinations cho n filters.
List accumulation cho phép combine tùy ý.

**Giải thích `selectinload` cho pagination:**
```python
stmt = stmt.options(selectinload(Transaction.category))
          .offset((page - 1) * size).limit(size)
```
`selectinload` emit 2 queries thay vì JOIN:
1. `SELECT * FROM transactions WHERE ... LIMIT 10`
2. `SELECT * FROM categories WHERE id IN (1, 2, 3, ...)`

So với JOIN: nếu category có nhiều transactions, JOIN sẽ duplicate data.

**Kiến thức áp dụng:** Khối 11 — selectinload, pagination

---

### Bước 4.3 — ReportRepository

**Làm gì:** Viết `app/repositories/report_repo.py` với 3 aggregate queries.

**Giải thích `case()` trong monthly report:**
```python
income = func.sum(
    case((Transaction.type == "income", Transaction.amount), else_=0)
)
expense = func.sum(
    case((Transaction.type == "expense", Transaction.amount), else_=0)
)
```
**Tại sao không query 2 lần?** Một query GROUP BY month, dùng CASE để split income/expense
trong cùng row → 12 rows cho 12 tháng, thay vì 24 rows (2 type × 12 tháng).

**Giải thích `extract("year", Transaction.transaction_date)`:**
SQLAlchemy cross-DB way để lấy year/month từ DATE column.
`EXTRACT(YEAR FROM transaction_date)` trong SQL thuần.

**Kiến thức áp dụng:** Khối 11 — func.sum, group_by, extract

---

## Kiến Thức Áp Dụng Trong Phase Này

| Kiến thức | Áp dụng cụ thể |
|----------|---------------|
| `select(Model)` | SQLAlchemy 2.0 query style |
| `session.execute()` + `.scalars()` | Async query execution |
| `session.scalar()` | Lấy single value (count) |
| `selectinload()` | Eager load relationship, tránh N+1 |
| `func.sum()`, `func.count()` | SQL aggregate |
| `group_by()`, `extract()` | Grouping và date extraction |
| `case()` | Conditional aggregate (CASE WHEN) |

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
