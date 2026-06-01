# Phase 7 — Seed & Smoke Test

## Trạng Thái

- [ ] Đang làm
- [x] Hoàn thành

**Bắt đầu:** 2026-06-02  
**Kết thúc:** 2026-06-02

---

## Tổng Quan Phase Này

**Làm gì:** Tạo seed data và chạy smoke test toàn bộ API bằng curl.

**Smoke test ≠ Unit test:**
- Unit test: test từng function riêng lẻ với mock
- Smoke test: test toàn bộ flow thực tế — server chạy, DB thật, request thật
- Smoke test bắt lỗi integration mà unit test bỏ sót

**Kết quả mong đợi:** Tất cả 16 test cases PASS.

---

## Seed Data

**File:** `seed.py` — chạy một lần để tạo dữ liệu mẫu:
```bash
uv run python seed.py
```

**Categories tạo:**
| id | name | type | icon | color |
|----|------|------|------|-------|
| 1 | Lương | income | 💰 | #4CAF50 |
| 2 | Freelance | income | 💻 | #2196F3 |
| 3 | Ăn uống | expense | 🍜 | #FF5722 |
| 4 | Di chuyển | expense | 🚗 | #FF9800 |
| 5 | Giải trí | expense | 🎮 | #9C27B0 |
| 6 | Tiết kiệm | expense | 🏦 | #607D8B |

**Transactions tạo:** 8 transactions (tháng 5 + tháng 6/2026).

**Lệnh chạy server:**
```bash
uv run uvicorn app.main:app --reload
```

---

## Bug Phát Hiện Khi Test

**Bug:** `GET /categories/?type=income` trả về tất cả 6 categories thay vì 2.

**Nguyên nhân:**
- `CategoryRepository.get_all()` không có param `type`
- Router `list_categories()` không khai báo query param `type`

**Fix:**
1. Thêm `type: str | None = None` vào `CategoryRepository.get_all()`
2. Thêm `type: Optional[Literal["income","expense"]] = Query(None)` vào router

---

## Smoke Test Checklist

Chạy lần lượt — có dependency giữa các TC.

### Categories

- [x] **TC-01** `GET /api/v1/categories/` → 200, 6 items
- [x] **TC-02** `GET /api/v1/categories/?type=income` → 200, 2 items (Lương, Freelance)
- [x] **TC-03** `GET /api/v1/categories/1` → 200, name="Lương"
- [x] **TC-04** `GET /api/v1/categories/999` → 404
- [x] **TC-05** `POST /api/v1/categories/` body hợp lệ → 201, id=7
- [x] **TC-06** `POST /api/v1/categories/` thiếu `name` → 422
- [x] **TC-07** `POST /api/v1/categories/` `type="invalid"` → 422
- [x] **TC-08** `PATCH /api/v1/categories/1` đổi name → 200, name="Lương Updated"
- [x] **TC-09** `DELETE /api/v1/categories/7` (Test Cat, không có transaction) → 204

### Transactions

- [x] **TC-10** `POST /api/v1/transactions/` với `category_id=1` → 201, `type="income"` (auto-derived)
- [x] **TC-11** `POST /api/v1/transactions/` với `category_id=999` → 404
- [x] **TC-12** `GET /api/v1/transactions/` → 200, 9 items
- [x] **TC-13** `GET /api/v1/transactions/?type=expense&page=1&size=5` → 200, 5 items expense
- [x] **TC-14** `DELETE /api/v1/categories/3` (Ăn uống có transactions) → 400, `error_code="BUSINESS"`
- [x] **TC-15** `DELETE /api/v1/transactions/9` → 204

### Reports

- [x] **TC-16** `GET /api/v1/reports/summary` → 200, `balance=30200000.00`

---

## Kết Quả Smoke Test

| TC | Endpoint | Expected | Actual | Pass/Fail |
|----|----------|----------|--------|-----------|
| 01 | GET /categories/ | 200, 6 items | 200, 6 items | ✅ PASS |
| 02 | GET /categories/?type=income | 200, 2 items | 200, 2 items | ✅ PASS |
| 03 | GET /categories/1 | 200, name=Lương | 200, name=Lương | ✅ PASS |
| 04 | GET /categories/999 | 404 | 404 | ✅ PASS |
| 05 | POST /categories/ | 201 | 201, id=7 | ✅ PASS |
| 06 | POST /categories/ (no name) | 422 | 422 | ✅ PASS |
| 07 | POST /categories/ (bad type) | 422 | 422 | ✅ PASS |
| 08 | PATCH /categories/1 | 200, name updated | 200, name=Lương Updated | ✅ PASS |
| 09 | DELETE /categories/7 | 204 | 204 | ✅ PASS |
| 10 | POST /transactions/ | 201, type=income | 201, type=income | ✅ PASS |
| 11 | POST /transactions/ (bad cat) | 404 | 404 | ✅ PASS |
| 12 | GET /transactions/ | 200 | 200, 9 items | ✅ PASS |
| 13 | GET /transactions/?filter | 200, expense only | 200, 5 expense items | ✅ PASS |
| 14 | DELETE /categories/3 (has tx) | 400 | 400, BUSINESS error | ✅ PASS |
| 15 | DELETE /transactions/9 | 204 | 204 | ✅ PASS |
| 16 | GET /reports/summary | 200, balance correct | 200, balance=30200000.00 | ✅ PASS |

**Tổng: 16/16 PASS**

---

## Swagger UI

Có thể test API trực tiếp trên browser (không cần curl):

```
http://127.0.0.1:8000/docs
```

---

## Điểm Rút Ra

- Smoke test chạy thực tế phát hiện bug `type` filter bị thiếu — unit test với mock sẽ không bắt được vì mock không chạy real query
- `DELETE /categories` trả 204 No Content khi thành công, 400 khi vi phạm business rule (có transactions) — cả hai đều là expected behavior, cần test cả hai case
- `error_code` trong response bị truncate do cách generate: `type(exc).__name__.replace("Exception","").upper()` → `NotFoundException` → `"NOTFOUND"`, `BusinessException` → `"BUSINESS"`

---

## Lỗi Gặp Phải

| # | Lỗi | Fix | Ghi chú |
|---|-----|-----|---------|
| 1 | `sqlite_sequence` không tồn tại khi DB rỗng | Bỏ dòng reset sequence — SQLite tự reset khi bảng rỗng | Chỉ xảy ra lần đầu seed |
| 2 | `GET /categories/?type=income` trả về tất cả | Thêm `type` param vào `CategoryRepository.get_all()` và router | Phát hiện qua TC-02 |
