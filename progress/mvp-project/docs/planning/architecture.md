# Architecture Decisions

> Ghi lại **tại sao** chọn kiến trúc này, không chỉ là kiến trúc là gì.
> Mỗi quyết định đều có lý do — nhìn lại sẽ hiểu trade-off.

---

## Layered Architecture

```
Router → Repository → ORM Model → Database
   ↓          ↓
Schema    Session (via Depends)
```

**Tại sao không để logic trong Router?**
Router chỉ nên làm: nhận request, validate, gọi repository, trả response.
Business logic (check active transactions trước khi soft-delete category) nằm trong Repository.
Nếu để trong Router, sau này muốn reuse logic đó (ví dụ từ CLI) sẽ không được.

---

## Repository Pattern

**Quyết định:** Mỗi model có 1 repository class riêng.

**Lý do:**
- Router không gọi SQLAlchemy trực tiếp → dễ test (mock repository)
- Tập trung query logic vào 1 chỗ → dễ tối ưu sau này
- Rõ ràng: `CategoryRepository.soft_delete()` vs một đống query rải trong router

---

## Soft Delete

**Quyết định:** Dùng `is_deleted=True` thay vì `DELETE` thực sự.

**Lý do:**
- Transaction đã delete vẫn còn trong báo cáo lịch sử
- Dễ recover nếu xóa nhầm
- Không break foreign key constraint nếu category bị xóa mà transaction vẫn reference

**Trade-off:** Query mặc định phải luôn thêm `WHERE is_deleted = false` — dễ quên.

---

## Transaction.type Tự Động

**Quyết định:** `type` của Transaction (income/expense) không nhận từ client — tự lấy từ Category.

**Lý do:**
- Category đã có `type` → Transaction phải match → nếu client tự set dễ mismatch
- Ví dụ: Category "Lương" là income nhưng client gửi type=expense → sai
- Auto-derive đảm bảo consistency, client không cần biết

---

## Async SQLAlchemy

**Quyết định:** Dùng `AsyncSession` thay vì sync Session.

**Lý do:**
- FastAPI natively async → dùng sync Session sẽ block event loop
- SQLite + aiosqlite cho dev, PostgreSQL + asyncpg cho production
- Pattern trong Khối 11

**Trade-off:** Cú pháp phức tạp hơn (`await session.execute(select(Model))`), khó debug hơn sync.

---

## Alembic cho Migration

**Quyết định:** Dùng Alembic, không dùng `Base.metadata.create_all()`.

**Lý do:**
- `create_all()` không track history — không biết DB đang ở version nào
- Alembic cho phép rollback, upgrade incremental
- `render_as_batch=True` cần thiết cho SQLite (không support ALTER TABLE natively)
