# SQLAlchemy Notes

> Kiến thức rút ra từ thực tế khi build project.
> Khác với lý thuyết trong Khối 11 — đây là những điểm "tự mình phát hiện".

---

## Mapped[T] vs Column (style cũ)

```python
# Cũ (SQLAlchemy 1.x)
name = Column(String, nullable=False)

# Mới (SQLAlchemy 2.0) — dùng trong project này
name: Mapped[str] = mapped_column()
icon: Mapped[str | None] = mapped_column()  # nullable
```

**Tại sao 2.0 style tốt hơn?**
- IDE autocomplete hoạt động (biết `category.name` là `str`)
- `Mapped[str | None]` rõ ràng hơn `nullable=True`
- Type checker (mypy, pyright) có thể catch lỗi

---

## Session Lifecycle

```
Request đến
    → FastAPI gọi get_db() generator
    → yield session ← endpoint nhận session này
    → endpoint làm việc
    → endpoint return
    → code sau yield chạy: session.close()
```

**Sai lầm phổ biến:** Lưu session vào biến global hoặc singleton.
Mỗi request phải có session riêng — session không thread-safe.

---

## selectinload vs joinedload vs lazy

| Strategy | SQL | Dùng khi |
|----------|-----|---------|
| `lazy="select"` (default) | 1 query per access | Không cần relationship thường xuyên |
| `selectinload` | 2 queries (IN clause) | Cần relationship, nhiều rows |
| `joinedload` | 1 query với JOIN | Cần relationship, ít rows, 1-to-1 |

**Trong project này:** Dùng `selectinload(Transaction.category)` vì:
- Pagination → mỗi page 20 transactions → IN clause với 20 IDs
- JOIN sẽ duplicate transaction data nếu category có nhiều transactions

---

## model_dump cho PATCH

```python
# Chỉ update field client gửi
update_data = schema.model_dump(exclude_unset=True)
for key, value in update_data.items():
    setattr(db_obj, key, value)
```

`exclude_unset=True` → loại bỏ field không có trong request body.
Nếu không dùng → PATCH sẽ overwrite mọi field bằng default value của schema.

---

## Async Pattern

```python
# Query nhiều rows
result = await session.execute(select(Category))
categories = result.scalars().all()

# Query 1 row
result = await session.execute(select(Category).where(Category.id == id))
category = result.scalar_one_or_none()

# Count
count = await session.scalar(select(func.count(Transaction.id)))
```

---

## Những Điều Tự Học Được

*(Append khi phát hiện insight mới)*

- 
- 
