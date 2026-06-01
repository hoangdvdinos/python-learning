# Phase 5 — Routers

## Trạng Thái

- [ ] Đang làm
- [x] Hoàn thành

**Bắt đầu:** 2026-06-02  
**Kết thúc:** 2026-06-02

---

## Tổng Quan Phase Này

**Làm gì:** Viết 3 APIRouter files — categories, transactions, reports.

**Router chỉ làm 3 việc:**
1. Nhận request (path params, query params, body)
2. Gọi repository
3. Trả response

**Không có logic nào trong router** — tất cả đã ở repository.

**Kết quả mong đợi:** Import routers không lỗi:
```bash
uv run python -c "from app.routers.categories import router; print(len(router.routes), 'routes')"
# Kết quả: 5 routes
```

---

## Các Bước Thực Hiện

### Bước 5.1 — Categories Router

**Làm gì:** Viết `app/routers/categories.py` với 5 endpoints: list, get, create, update, delete.

**Giải thích `Annotated` dependency pattern:**
```python
def get_category_repo(session: Annotated[AsyncSession, Depends(get_db)]) -> CategoryRepository:
    return CategoryRepository(session)

CategoryRepoDep = Annotated[CategoryRepository, Depends(get_category_repo)]

@router.get("/")
async def list_categories(repo: CategoryRepoDep):
    ...
```
**Tại sao dùng `Annotated` thay vì `Depends` trực tiếp?**
- Khai báo 1 lần (`CategoryRepoDep`), dùng ở mọi endpoint
- Type-safe: IDE biết `repo` là `CategoryRepository`
- Function signature gọn hơn

**Endpoints:**
| Method | Path | Status Code | Mô tả |
|--------|------|-------------|-------|
| GET | `/categories/` | 200 | Lấy danh sách |
| GET | `/categories/{id}` | 200 | Lấy 1 category |
| POST | `/categories/` | **201** | Tạo mới |
| PATCH | `/categories/{id}` | 200 | Cập nhật |
| DELETE | `/categories/{id}` | **204** | Soft delete |

**Kiến thức áp dụng:** Khối 11 — Depends, Annotated, Khối 9 — APIRouter

**Lệnh:** *(không có lệnh shell — chỉ tạo file)*

---

### Bước 5.2 — Transactions Router

**Làm gì:** Viết `app/routers/transactions.py` với Query params cho filtering và pagination.

**Giải thích Query params với validation:**
```python
@router.get("/")
async def list_transactions(
    type: Optional[Literal["income", "expense"]] = Query(None),
    category_id: Optional[int] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
```
**Tại sao `ge=1` cho page và `le=100` cho size?**
- `page=0` sẽ tính offset âm → sai logic
- `size=999999` → trả về quá nhiều data → bảo vệ server
- FastAPI validate tự động → trả 422 nếu vi phạm

**Endpoints:**
| Method | Path | Query Params | Mô tả |
|--------|------|-------------|-------|
| GET | `/transactions/` | type, category_id, date_from, date_to, page, size | Lấy danh sách với filter |
| GET | `/transactions/{id}` | — | Lấy 1 transaction |
| POST | `/transactions/` | — | Tạo mới |
| PATCH | `/transactions/{id}` | — | Cập nhật |
| DELETE | `/transactions/{id}` | — | Soft delete |

**Kiến thức áp dụng:** Khối 6 — Query params, Khối 8 — Validation

**Lệnh:** *(không có lệnh shell — chỉ tạo file)*

---

### Bước 5.3 — Reports Router

**Làm gì:** Viết `app/routers/reports.py` với 3 GET endpoints.

**Tại sao reports là `GET` không phải `POST`?**
- Reports không tạo/thay đổi data → `GET` là đúng HTTP semantics
- `GET` có thể cache (nếu thêm cache layer sau này)

**Endpoints:**
| Method | Path | Mô tả |
|--------|------|-------|
| GET | `/reports/summary` | Tổng income/expense/balance |
| GET | `/reports/monthly` | Breakdown theo tháng |
| GET | `/reports/by-category` | Breakdown theo danh mục |

**Lệnh:** *(không có lệnh shell — chỉ tạo file)*

---

### Bước 5.4 — `__init__.py` cho routers

**Làm gì:** Export tất cả routers từ `app/routers/__init__.py`.

**Verify:**
```bash
uv run python -c "
from app.routers.categories import router as cr
from app.routers.transactions import router as tr
from app.routers.reports import router as rr
print('categories:', len(cr.routes), 'routes')
print('transactions:', len(tr.routes), 'routes')
print('reports:', len(rr.routes), 'routes')
"
# Kết quả:
# categories: 5 routes
# transactions: 5 routes
# reports: 3 routes
```

---

## Kiến Thức Áp Dụng Trong Phase Này

| Kiến thức | Áp dụng cụ thể |
|----------|---------------|
| `APIRouter` | Tách routes theo domain (categories, transactions, reports) |
| `Depends()` | Inject repository vào endpoint |
| `Annotated[T, Depends(...)]` | Type-safe dependency, khai báo 1 lần dùng nhiều nơi |
| `Query(default, ge=, le=)` | Validated query parameters với constraints |
| `response_model=` | Pydantic serialize và filter output |
| `status_code=201` | Đúng HTTP status cho POST (tạo mới) |
| `status_code=204` | Đúng HTTP status cho DELETE (no content) |

---

## Điểm Rút Ra

- Router không chứa logic — chỉ bridge giữa HTTP và repository; mọi business rule đã ở repository
- `Annotated[T, Depends(...)]` khai báo 1 lần thành type alias (`CategoryRepoDep`) → tránh lặp lại `Depends(get_category_repo)` ở mỗi endpoint
- DELETE trả `204 No Content` → không có response body; nếu return `None` là đúng, không phải lỗi

---

## Lỗi Gặp Phải

| # | Lỗi | Fix | Entry trong error-log |
|---|-----|-----|-----------------------|
| — | Không gặp lỗi trong phase này | — | — |
