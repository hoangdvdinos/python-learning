# API Design

> Contract được quyết định trước khi code.
> Router implement đúng contract này, không được tự ý thêm/bỏ field.

---

## Base URL

```
http://localhost:8000/api/v1
```

---

## Categories

| Method | Path | Mô tả |
|--------|------|-------|
| GET | `/categories` | Lấy danh sách (filter: type, is_active) |
| GET | `/categories/{id}` | Lấy 1 category |
| POST | `/categories` | Tạo mới |
| PATCH | `/categories/{id}` | Cập nhật |
| DELETE | `/categories/{id}` | Soft delete |

**Request — POST /categories**
```json
{
  "name": "Lương",
  "type": "income",
  "icon": "💰",
  "color": "#4CAF50"
}
```

**Response — CategoryResponse**
```json
{
  "id": 1,
  "name": "Lương",
  "type": "income",
  "icon": "💰",
  "color": "#4CAF50",
  "is_active": true,
  "created_at": "2026-05-31T10:00:00"
}
```

---

## Transactions

| Method | Path | Mô tả |
|--------|------|-------|
| GET | `/transactions` | Lấy danh sách (filter: type, category_id, date range, page/size) |
| GET | `/transactions/{id}` | Lấy 1 transaction |
| POST | `/transactions` | Tạo mới |
| PATCH | `/transactions/{id}` | Cập nhật |
| DELETE | `/transactions/{id}` | Soft delete |

**Request — POST /transactions**
```json
{
  "category_id": 1,
  "amount": 15000000,
  "note": "Lương tháng 5",
  "transaction_date": "2026-05-31"
}
```

> `type` không có trong request — tự derive từ category.

**Response — TransactionResponse**
```json
{
  "id": 1,
  "category_id": 1,
  "category_name": "Lương",
  "amount": 15000000,
  "type": "income",
  "note": "Lương tháng 5",
  "transaction_date": "2026-05-31",
  "created_at": "2026-05-31T10:00:00"
}
```

---

## Reports

| Method | Path | Query Params | Mô tả |
|--------|------|-------------|-------|
| GET | `/reports/summary` | `year`, `month` (optional) | Tổng income/expense/balance |
| GET | `/reports/monthly` | `year` (required) | Breakdown 12 tháng |
| GET | `/reports/by-category` | `year`, `month` (optional), `type` | Tổng theo từng category |

**Response — GET /reports/summary?year=2026&month=5**
```json
{
  "total_income": 20000000,
  "total_expense": 8500000,
  "balance": 11500000,
  "period": "2026-05"
}
```

---

## Error Format

Tất cả lỗi trả về cùng 1 format:

```json
{
  "error_code": "NOT_FOUND",
  "message": "Category with id 99 not found",
  "detail": null
}
```

| HTTP Status | error_code | Khi nào |
|-------------|-----------|---------|
| 404 | NOT_FOUND | Resource không tồn tại |
| 422 | VALIDATION_ERROR | Pydantic validation fail |
| 400 | BUSINESS_ERROR | Vi phạm business rule |
| 500 | INTERNAL_ERROR | Unexpected server error |
