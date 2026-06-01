# Phase 3 — Schemas & Exceptions

## Trạng Thái

- [ ] Đang làm
- [x] Hoàn thành

**Bắt đầu:** 2026-05-31  
**Kết thúc:** 2026-05-31

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

**Code thực tế:**
```python
class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class NotFoundException(AppException):
    def __init__(self, resource: str, resource_id: int | str) -> None:
        super().__init__(
            message=f"{resource} with id={resource_id} not found",
            status_code=404,
        )

class BusinessException(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=400)
```

**Lệnh:** *(không có lệnh shell — chỉ tạo file)*

---

### Bước 3.2 — Category Schemas

**Làm gì:** Viết `app/schemas/category.py` với `CategoryCreate`, `CategoryUpdate`, `CategoryResponse`.

**Giải thích `Literal["income", "expense"]`:**
- `str` cho phép mọi string → client có thể gửi `type: "random_value"`
- `Literal["income", "expense"]` → Pydantic validate ngay, trả 422 nếu sai
- Không cần viết validator thủ công

**Giải thích `model_config = ConfigDict(from_attributes=True)`:**
- Mặc định Pydantic chỉ đọc dict
- `from_attributes=True` → cho phép đọc từ ORM object (SQLAlchemy model)
- Cần thiết khi làm `CategoryResponse.model_validate(db_category)`

**Kiến thức áp dụng:** Khối 5 — Pydantic v2, Khối 8 — Validation

**Code thực tế:**
```python
class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: Literal["income", "expense"]
    icon: str | None = Field(default=None, max_length=50)
    color: str | None = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")

class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    icon: str | None = Field(default=None, max_length=50)
    color: str | None = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")

class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    type: str
    icon: str | None
    color: str | None
```

**Lệnh:** *(không có lệnh shell — chỉ tạo file)*

---

### Bước 3.3 — Transaction Schemas

**Làm gì:** Viết `app/schemas/transaction.py` với `TransactionCreate`, `TransactionUpdate`, `TransactionResponse`.

**Tại sao `TransactionCreate` không có field `type`?**
- `type` được derive từ category (income/expense theo category)
- Nếu để client gửi → dễ mismatch với category type
- Pydantic schema là "contract" với client — không expose field không cần thiết

**Giải thích `TransactionResponse` có `category: CategoryResponse`:**
- DB lưu `category_id` (foreign key)
- Client muốn thấy tên và thông tin category, không chỉ ID
- `category` được populate tự động từ relationship `lazy="selectin"` ở model

**Kiến thức áp dụng:** Khối 5 — Pydantic nested models

**Code thực tế:**
```python
class TransactionCreate(BaseModel):
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    description: str | None = Field(default=None)
    transaction_date: date
    category_id: int

class TransactionUpdate(BaseModel):
    amount: Decimal | None = Field(default=None, gt=0, decimal_places=2)
    description: str | None = None
    transaction_date: date | None = None
    category_id: int | None = None

class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    amount: Decimal
    type: str
    description: str | None
    transaction_date: date
    category_id: int
    category: CategoryResponse
```

**Lệnh:** *(không có lệnh shell — chỉ tạo file)*

---

### Bước 3.4 — Report Schemas

**Làm gì:** Viết `app/schemas/report.py` với `SummaryResponse`, `MonthlyResponse`, `ByCategoryResponse`.

**Tại sao cần schemas riêng cho reports?**
- Report data không map 1-1 với bất kỳ ORM model nào
- Là kết quả aggregate (SUM, GROUP BY) → cần schema riêng
- Không dùng `from_attributes=True` — data từ dict/tuple, không phải ORM object

**Code thực tế:**
```python
class SummaryResponse(BaseModel):
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal

class MonthlyItem(BaseModel):
    year: int
    month: int
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal

class MonthlyResponse(BaseModel):
    items: list[MonthlyItem]

class ByCategoryItem(BaseModel):
    category_id: int
    category_name: str
    type: str
    total: Decimal

class ByCategoryResponse(BaseModel):
    items: list[ByCategoryItem]
```

**Lệnh:** *(không có lệnh shell — chỉ tạo file)*

---

### Bước 3.5 — `__init__.py` cho schemas

**Làm gì:** Export tất cả schemas từ `app/schemas/__init__.py`.

**Lý do:** Các router chỉ cần `from app.schemas import CategoryCreate` thay vì import từng file riêng.

**Lệnh verify:**
```bash
uv run python -c "from app.schemas.category import CategoryCreate; print(CategoryCreate.model_fields)"
uv run python -c "from app.core.exceptions import NotFoundException; print(NotFoundException('Category', 1))"
```

---

## Kiến Thức Áp Dụng Trong Phase Này

| Kiến thức | Áp dụng cụ thể |
|----------|---------------|
| `BaseModel` | Tất cả schemas kế thừa |
| `Field(...)` | Validation: min/max, pattern, description |
| `Literal[...]` | Constrain `type` tới `"income"` hoặc `"expense"` |
| `model_config` | `from_attributes=True` cho ORM compat |
| `model_dump(exclude_unset=True)` | PATCH — chỉ update field client gửi (dùng ở repository) |
| Custom exceptions | Separation of concerns giữa layers |
| Nested schema | `TransactionResponse` chứa `CategoryResponse` |

---

## Điểm Rút Ra

- `CategoryUpdate` không có field `type` — category type không được phép đổi sau khi tạo (business rule)
- `TransactionCreate` không có field `type` — type được kế thừa từ category để tránh mismatch
- `from_attributes=True` chỉ cần ở Response schema, không cần ở Create/Update vì chúng chỉ nhận dict từ request

---

## Lỗi Gặp Phải

| # | Lỗi | Fix | Entry trong error-log |
|---|-----|-----|-----------------------|
| — | Không gặp lỗi trong phase này | — | — |
