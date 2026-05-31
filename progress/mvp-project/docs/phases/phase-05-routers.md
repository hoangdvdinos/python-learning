# Phase 5 — Routers

## Trạng Thái

- [ ] Đang làm
- [ ] Hoàn thành

**Bắt đầu:** ___________  
**Kết thúc:** ___________

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
# Mong đợi: 5 routes
```

---

## Các Bước Thực Hiện

### Bước 5.1 — Categories Router

**Làm gì:** Viết `app/routers/categories.py`.

**Giải thích `Annotated` dependency pattern:**
```python
CategoryRepoDep = Annotated[CategoryRepository, Depends(get_category_repo)]

@router.get("/")
async def list_categories(repo: CategoryRepoDep):
    ...
```
**Tại sao dùng `Annotated` thay vì `Depends` trực tiếp?**
- Khai báo 1 lần, dùng ở nhiều endpoints
- Type-safe: IDE biết `repo` là `CategoryRepository`
- Cleaner function signature

**Kiến thức áp dụng:** Khối 11 — Depends, Annotated

---

### Bước 5.2 — Transactions Router

**Làm gì:** Viết `app/routers/transactions.py` với Query params cho filtering.

**Giải thích Query params với Optional:**
```python
@router.get("/")
async def list_transactions(
    type: Optional[Literal["income", "expense"]] = Query(None),
    category_id: Optional[int] = Query(None),
    date_from: Optional[date] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
```
**Tại sao `ge=1` cho page và `le=100` cho size?**
- Ngăn client gửi `page=0` hoặc `size=999999`
- FastAPI validate tự động → trả 422 nếu sai
- `le=100` giới hạn max records per page → bảo vệ server

**Kiến thức áp dụng:** Khối 6 — Query params, Khối 8 — Validation

---

### Bước 5.3 — Reports Router

**Làm gì:** Viết `app/routers/reports.py`.

**Tại sao reports là `GET` không phải `POST`?**
- Reports không tạo/thay đổi data → `GET` là đúng HTTP semantics
- `GET` có thể cache (nếu thêm cache layer sau này)
- Query params phù hợp với filter (year, month, type)

---

## Kiến Thức Áp Dụng Trong Phase Này

| Kiến thức | Áp dụng cụ thể |
|----------|---------------|
| `APIRouter` | Tách routes theo domain |
| `Depends()` | Inject repository vào endpoint |
| `Annotated[T, Depends(...)]` | Type-safe dependency declaration |
| `Query(default, ge=, le=)` | Validated query parameters |
| `response_model=` | Pydantic serialize output |
| `status_code=201` | Đúng HTTP status cho POST |

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
