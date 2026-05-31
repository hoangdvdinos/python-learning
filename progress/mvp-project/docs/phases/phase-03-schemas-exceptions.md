# Phase 3 — Schemas & Exceptions

## Trạng Thái

- [ ] Đang làm
- [ ] Hoàn thành

**Bắt đầu:** ___________  
**Kết thúc:** ___________

---

## Tổng Quan Phase Này

**Làm gì:** Định nghĩa Pydantic schemas (contract của API) và custom exception classes.

**Tại sao làm trước repositories/routers?**
- Repository trả về data — cần schema để biết trả về dạng gì
- Router nhận request — cần schema để validate input
- Exception phải có trước khi repository raise nó

**Kết quả mong đợi:** Import schemas và exceptions không lỗi:
```bash
uv run python -c "from app.schemas.category import CategoryCreate; print(CategoryCreate.model_fields)"
```

---

## Các Bước Thực Hiện

### Bước 3.1 — Custom Exceptions

**Làm gì:** Viết `app/core/exceptions.py` với `AppException`, `NotFoundException`, `BusinessException`.

**Tại sao không dùng `HTTPException` trực tiếp trong repository?**
- Repository không nên biết về HTTP — đó là concern của layer trên
- `NotFoundException` → repository raise, router không cần handle
- Exception handler ở `main.py` convert sang `HTTPException` với format chuẩn

**Kiến thức áp dụng:** Khối 10 — Exception handlers

---

### Bước 3.2 — Category Schemas

**Làm gì:** Viết `app/schemas/category.py`.

**Giải thích `Literal["income", "expense"]`:**
- `str` cho phép mọi string → client có thể gửi `type: "random_value"`
- `Literal["income", "expense"]` → Pydantic validate ngay, trả 422 nếu sai
- Không cần viết validator thủ công

**Giải thích `model_config = ConfigDict(from_attributes=True)`:**
- Mặc định Pydantic chỉ đọc dict
- `from_attributes=True` → cho phép đọc từ ORM object (SQLAlchemy model)
- Cần thiết khi làm `CategoryResponse.model_validate(db_category)`

**Kiến thức áp dụng:** Khối 5 — Pydantic v2, Khối 8 — Validation

---

### Bước 3.3 — Transaction Schemas

**Làm gì:** Viết `app/schemas/transaction.py`.

**Tại sao `TransactionCreate` không có field `type`?**
- `type` được derive từ category (xem architecture.md)
- Nếu để client gửi → dễ mismatch với category type
- Pydantic schema là "contract" với client — không expose field không cần thiết

**Giải thích `TransactionResponse` có `category_name`:**
- DB lưu `category_id` (foreign key)
- Client muốn thấy tên, không phải ID
- `category_name` được populate từ `transaction.category.name` (nhờ relationship)

**Kiến thức áp dụng:** Khối 5 — Pydantic nested models

---

### Bước 3.4 — Report Schemas

**Làm gì:** Viết `app/schemas/report.py` với `SummaryResponse`, `MonthlyResponse`, `ByCategoryResponse`.

**Tại sao cần schemas riêng cho reports?**
- Report data không map 1-1 với bất kỳ ORM model nào
- Là kết quả aggregate (SUM, GROUP BY) → cần schema riêng
- Không dùng `from_attributes=True` — data từ dict/tuple, không phải ORM object

---

## Kiến Thức Áp Dụng Trong Phase Này

| Kiến thức | Áp dụng cụ thể |
|----------|---------------|
| `BaseModel` | Tất cả schemas kế thừa |
| `Field(...)` | Validation: min/max, pattern, description |
| `Literal[...]` | Constrain giá trị tới tập cụ thể |
| `model_config` | `from_attributes=True` cho ORM compat |
| `model_dump(exclude_unset=True)` | PATCH — chỉ update field client gửi |
| Custom exceptions | Separation of concerns giữa layers |

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
