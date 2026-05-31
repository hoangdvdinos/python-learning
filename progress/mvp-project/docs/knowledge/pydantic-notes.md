# Pydantic Notes

> Kiến thức Pydantic v2 rút ra từ project.

---

## model_config Quan Trọng

```python
class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
```

`from_attributes=True` cho phép:
```python
db_category = await repo.get_by_id(1)  # SQLAlchemy ORM object
response = CategoryResponse.model_validate(db_category)  # Works!
```

Không có flag này → `ValidationError: Input should be a valid dictionary`.

---

## Literal Type cho Enum-like Values

```python
from typing import Literal

type: Literal["income", "expense"]
```

vs dùng Python `Enum`:
- `Literal` đơn giản hơn, không cần import/define class riêng
- Pydantic serialize thành string thay vì `"income"` vs `TransactionType.income`
- Dùng `Enum` khi cần nhiều method/property trên value

---

## model_dump Options

```python
# Tất cả field
schema.model_dump()
# → {"name": "Lương", "type": "income", "icon": null, "color": null}

# Chỉ field được set (PATCH)
schema.model_dump(exclude_unset=True)
# → {"name": "Lương mới"}  # nếu chỉ name được gửi

# Bỏ field None
schema.model_dump(exclude_none=True)
# → {"name": "Lương", "type": "income"}
```

---

## Field Validators

```python
from pydantic import Field, field_validator

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    color: str | None = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    
    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        return v.strip()
```

`Field(...)` = required (không có default).
`pattern=` = regex validation.
`@field_validator` = custom logic.

---

## Nested Response Schema

```python
class TransactionResponse(BaseModel):
    id: int
    category_id: int
    category_name: str  # từ transaction.category.name
    amount: float
    
    model_config = ConfigDict(from_attributes=True)
```

SQLAlchemy object có relationship → Pydantic tự traverse nếu `from_attributes=True`.
Nhưng an toàn hơn là populate thủ công trong repository.

---

## Những Điều Tự Học Được

*(Append khi phát hiện insight mới)*

- 
- 
