# 5W1H — alembic.ini

**Ai (Who):**

- Công cụ Alembic và developer/CI chạy lệnh migration.
- File được đọc bởi [alembic/env.py](alembic/env.py).

**Cái gì (What):**

- Tệp cấu hình cho Alembic (database migrations). Nó chứa:
  - `script_location` — nơi chứa script migration (`alembic/`).
  - `sqlalchemy.url` — URL kết nối database (ở project này: `sqlite+aiosqlite:///./finance.db`).
  - Các cấu hình logging, `path_separator`, và `post_write_hooks`.

**Khi nào (When):**

- Khi bạn tạo migration: `alembic revision --autogenerate`.
- Khi áp dụng migration: `alembic upgrade head`.
- Khi `alembic/env.py` được khởi chạy (ví dụ trong CI hoặc local dev).

**Ở đâu (Where):**

- File nằm ở repository root: [alembic.ini](alembic.ini).
- Script migration nằm trong thư mục `alembic/`, ví dụ: [alembic/versions/0e402f9da6d8_init_categories_and_transactions.py](alembic/versions/0e402f9da6d8_init_categories_and_transactions.py).

**Tại sao (Why):**

- Để quản lý lịch sử thay đổi schema của database theo dạng migration có thể tái tạo.
- Giúp đồng bộ schema giữa máy dev, staging, và production.
- Hỗ trợ autogenerate từ model metadata để giảm sai sót thủ công.

**Như thế nào (How):**

- `alembic.ini` cung cấp thông tin (ví dụ `sqlalchemy.url`) cho `alembic/env.py` để kết nối và chạy migration.
- Thực thi lệnh Alembic từ terminal:

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
alembic history --verbose
```

- Lưu ý: project này dùng `sqlite+aiosqlite` — đảm bảo `env.py` xử lý kết nối bất đồng bộ nếu cần.

---

Nếu bạn muốn, tôi có thể:

- Thêm hướng dẫn ngắn vào `README.md` để ghi lại các lệnh Alembic phổ biến.
- Hoặc cập nhật `alembic/env.py` để làm rõ cách lấy `sqlalchemy.url` từ `alembic.ini` hoặc biến môi trường.
