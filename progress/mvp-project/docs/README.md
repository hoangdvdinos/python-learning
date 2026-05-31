# Project Docs — Personal Finance Tracker

> Thư mục này là **single source of truth** cho toàn bộ quá trình xây dựng project.
> Mục đích: Nhìn lại bất kỳ lúc nào đều biết *tại sao*, *làm gì*, *học được gì*, *gặp lỗi gì*.

---

## Cấu Trúc

```
docs/
├── README.md                        ← file này — index toàn bộ
│
├── planning/                        ← quyết định TRƯỚC khi code
│   ├── project-overview.md          ← scope, mục tiêu, out-of-scope
│   ├── architecture.md              ← tại sao chọn kiến trúc này
│   └── api-design.md                ← endpoint contract trước khi implement
│
├── phases/                          ← ghi lại TRONG KHI code
│   ├── phase-01-setup.md
│   ├── phase-02-models-migration.md
│   ├── phase-03-schemas-exceptions.md
│   ├── phase-04-repositories.md
│   ├── phase-05-routers.md
│   ├── phase-06-main.md
│   └── phase-07-seed-test.md
│
├── errors/                          ← ghi lại LỖI gặp phải
│   └── error-log.md                 ← tất cả lỗi + cách fix
│
├── knowledge/                       ← kiến thức RÚT RA sau khi làm
│   ├── sqlalchemy-notes.md
│   ├── pydantic-notes.md
│   └── fastapi-patterns.md
│
└── retrospective/
    └── final-review.md              ← nhìn lại toàn bộ sau khi xong
```

---

## Cách Sử Dụng

| Thời điểm | Việc cần làm |
|-----------|-------------|
| Trước khi bắt đầu phase | Đọc `planning/` để nhớ lại quyết định ban đầu |
| Trong khi code | Cập nhật `phases/phase-XX.md` — ghi ngay khi làm xong 1 bước |
| Khi gặp lỗi | Mở `errors/error-log.md`, append entry mới |
| Sau khi xong phase | Viết phần **Kiến Thức Áp Dụng** và **Điểm Rút Ra** |
| Sau khi xong project | Viết `retrospective/final-review.md` |

---

## Quick Links

- [Project Overview](planning/project-overview.md)
- [Architecture Decisions](planning/architecture.md)
- [Error Log](errors/error-log.md)
- [Final Review](retrospective/final-review.md)
