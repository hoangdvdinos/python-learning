# FastAPI Patterns

> Các pattern tái sử dụng, rút ra từ quá trình build project.

---

## Annotated Dependency Pattern

```python
# Khai báo 1 lần
DbSession = Annotated[AsyncSession, Depends(get_db)]
CategoryRepoDep = Annotated[CategoryRepository, Depends(get_category_repo)]

# Dùng ở nhiều chỗ
@router.get("/")
async def list_categories(repo: CategoryRepoDep): ...

@router.get("/{id}")
async def get_category(id: int, repo: CategoryRepoDep): ...
```

**Tại sao tốt hơn `Depends()` inline?**
- Type-safe: IDE biết type
- DRY: thay đổi 1 chỗ
- Readable: `repo: CategoryRepoDep` vs `repo: CategoryRepository = Depends(get_category_repo)`

---

## Response Model Pattern

```python
@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(body: CategoryCreate, repo: CategoryRepoDep):
    category = await repo.create(body)
    return category  # FastAPI tự serialize qua CategoryResponse
```

`response_model` làm 2 việc:
1. Serialize ORM object → dict theo schema
2. Filter out field không có trong schema (security)

---

## Soft Delete Pattern

```python
# Không bao giờ DELETE thực sự
async def soft_delete(self, id: int) -> None:
    obj = await self.get_by_id(id)  # raises 404 nếu không tồn tại
    obj.is_deleted = True
    await self.session.commit()
```

Mọi query đều thêm filter:
```python
select(Model).where(Model.is_deleted == False)
```

---

## Dynamic Filter Builder

```python
filters = [Transaction.is_deleted == False]  # base filter luôn có

if type:
    filters.append(Transaction.type == type)
if category_id:
    filters.append(Transaction.category_id == category_id)

stmt = select(Transaction).where(*filters)
```

Mỗi param là optional → accumulate thay vì if/else phức tạp.

---

## Exception Handler Registration

```python
# main.py
app.add_exception_handler(NotFoundException, not_found_handler)
app.add_exception_handler(BusinessException, business_error_handler)
app.add_exception_handler(Exception, generic_error_handler)  # fallback
```

Các layer dưới (repository) raise `NotFoundException` → không biết về HTTP.
`main.py` convert sang `JSONResponse` với status code phù hợp.

---

## Những Điều Tự Học Được

*(Append khi phát hiện insight mới)*

- 
- 
