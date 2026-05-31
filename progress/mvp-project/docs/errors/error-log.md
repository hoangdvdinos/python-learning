# Error Log

> Ghi lại mọi lỗi gặp trong quá trình triển khai.
> Mục đích: Không mất thời gian debug lại lỗi cũ. Nhìn vào đây biết ngay cách fix.

---

## Format Mỗi Entry

```
### ERR-XXX — [Tên lỗi ngắn gọn]

**Phase:** Phase X — tên phase
**Thời điểm:** Đang làm bước nào

**Triệu chứng:**
Error message thực tế

**Nguyên nhân:**
Tại sao lỗi xảy ra

**Fix:**
Làm gì để fix

**Bài học:**
Rút ra được gì, lần sau tránh làm gì
```

---

## Lỗi Đã Gặp

*(Append entry mới xuống dưới khi gặp lỗi)*

---

### ERR-001 — Template (Xóa khi có lỗi thực)

**Phase:** Phase 1 — Setup  
**Thời điểm:** Bước 1.3 — config.py

**Triệu chứng:**
```
pydantic_settings.env_settings.SettingsError: error loading .env file: ...
```

**Nguyên nhân:**
`.env` file không tồn tại trong thư mục hiện tại khi chạy lệnh.

**Fix:**
Chạy lệnh từ root của project (nơi có `.env`), không phải từ thư mục `app/`.

**Bài học:**
Luôn chạy `uv run` từ project root. Kiểm tra CWD bằng `pwd` nếu lỗi file-not-found.

---

## Thống Kê

| Phase | Số lỗi | Đã fix |
|-------|--------|--------|
| Phase 1 — Setup | 0 | 0 |
| Phase 2 — Models | 0 | 0 |
| Phase 3 — Schemas | 0 | 0 |
| Phase 4 — Repositories | 0 | 0 |
| Phase 5 — Routers | 0 | 0 |
| Phase 6 — main.py | 0 | 0 |
| Phase 7 — Test | 0 | 0 |

---

## Lỗi Thường Gặp Với FastAPI + SQLAlchemy

*(Reference nhanh — các lỗi phổ biến)*

| Lỗi | Nguyên nhân | Fix |
|-----|------------|-----|
| `greenlet_spawn` error | Dùng sync SQLAlchemy trong async context | Dùng `AsyncSession` thay vì `Session` |
| `DetachedInstanceError` | Truy cập relationship sau khi session closed | Dùng `selectinload()` khi query |
| `MissingGreenlet` | Chạy async code trong sync context | Wrap với `asyncio.run()` |
| `alembic.util.exc.CommandError` | Target_metadata không import models | Import models trong `alembic/env.py` |
| `422 Unprocessable Entity` | Request body không match schema | Kiểm tra Pydantic schema, đọc error detail |
| `ModuleNotFoundError` | Thiếu `__init__.py` trong package | Tạo file `__init__.py` trong thư mục |
