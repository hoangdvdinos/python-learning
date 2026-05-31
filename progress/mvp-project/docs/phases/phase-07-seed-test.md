# Phase 7 — Seed & Smoke Test

## Trạng Thái

- [ ] Đang làm
- [ ] Hoàn thành

**Bắt đầu:** ___________  
**Kết thúc:** ___________

---

## Tổng Quan Phase Này

**Làm gì:** Tạo seed data và chạy smoke test toàn bộ API bằng tay (hoặc script).

**Smoke test ≠ Unit test:**
- Unit test: test từng function riêng lẻ với mock
- Smoke test: test toàn bộ flow thực tế — server chạy, DB thật, request thật
- Smoke test bắt lỗi integration mà unit test bỏ sót

**Kết quả mong đợi:** Tất cả 16 test cases PASS.

---

## Seed Data

Chạy `seed.py` để tạo dữ liệu mẫu:
```bash
uv run python seed.py
```

**Categories tạo:**
| id | name | type |
|----|------|------|
| 1 | Lương | income |
| 2 | Freelance | income |
| 3 | Ăn uống | expense |
| 4 | Di chuyển | expense |
| 5 | Giải trí | expense |
| 6 | Tiết kiệm | expense |

---

## Smoke Test Checklist

Chạy theo đúng thứ tự này (có dependency):

### Categories

- [ ] **TC-01** `GET /api/v1/categories` → 200, trả về 6 categories
- [ ] **TC-02** `GET /api/v1/categories?type=income` → 200, trả về 2 categories
- [ ] **TC-03** `GET /api/v1/categories/1` → 200, name = "Lương"
- [ ] **TC-04** `GET /api/v1/categories/999` → 404, error_code = "NOT_FOUND"
- [ ] **TC-05** `POST /api/v1/categories` body hợp lệ → 201, trả về category mới
- [ ] **TC-06** `POST /api/v1/categories` body thiếu `name` → 422
- [ ] **TC-07** `POST /api/v1/categories` body `type = "invalid"` → 422
- [ ] **TC-08** `PATCH /api/v1/categories/1` đổi name → 200, name đã đổi
- [ ] **TC-09** `DELETE /api/v1/categories/5` (category không có transaction) → 200

### Transactions

- [ ] **TC-10** `POST /api/v1/transactions` với category_id=1 → 201, type="income" (auto-derived)
- [ ] **TC-11** `POST /api/v1/transactions` với category_id=999 → 404
- [ ] **TC-12** `GET /api/v1/transactions` → 200, trả về list
- [ ] **TC-13** `GET /api/v1/transactions?type=expense&page=1&size=5` → 200, đúng filter
- [ ] **TC-14** `DELETE /api/v1/categories/3` (category ĂN UỐNG đang có transaction) → 400, error_code = "BUSINESS_ERROR"
- [ ] **TC-15** `DELETE /api/v1/transactions/{id}` → 200, is_deleted=true

### Reports

- [ ] **TC-16** `GET /api/v1/reports/summary` → 200, balance = total_income - total_expense

---

## Kết Quả Smoke Test

| TC | Endpoint | Expected | Actual | Pass/Fail | Ghi chú |
|----|----------|----------|--------|-----------|---------|
| 01 | GET /categories | 200 | | | |
| 02 | GET /categories?type=income | 200, 2 items | | | |
| 03 | GET /categories/1 | 200, name=Lương | | | |
| 04 | GET /categories/999 | 404 | | | |
| 05 | POST /categories | 201 | | | |
| 06 | POST /categories (no name) | 422 | | | |
| 07 | POST /categories (bad type) | 422 | | | |
| 08 | PATCH /categories/1 | 200 | | | |
| 09 | DELETE /categories/5 | 200 | | | |
| 10 | POST /transactions | 201, type=income | | | |
| 11 | POST /transactions (bad cat) | 404 | | | |
| 12 | GET /transactions | 200 | | | |
| 13 | GET /transactions?filter | 200 | | | |
| 14 | DELETE /categories/3 (has tx) | 400 | | | |
| 15 | DELETE /transactions/{id} | 200 | | | |
| 16 | GET /reports/summary | 200 | | | |

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
