# Frontend Plan — Finance Tracker (Nuxt)

Bộ tài liệu **vừa-làm-vừa-hiểu** để xây frontend Nuxt cho backend FastAPI `finance-tracker`.
Viết cho người **mới học Nuxt** nhưng **đã rành Java/Spring + Laravel + Flutter** — nên có so sánh chéo liên tục.

## Triết lý

Mỗi phase = **1 thứ chạy được** + **vài khái niệm mới được giải thích kỹ**. Không nhảy phase. Cuối mỗi file có:
- **✅ Checklist** — việc cần làm.
- **🧠 Tự kiểm tra** — câu hỏi để chắc là *hiểu*, không chỉ copy code.

## Tech stack đã chốt

Nuxt (mới nhất) · TypeScript · **Nuxt UI** (component dựng sẵn) · Pinia (state) · Chart.js (biểu đồ) · `$fetch`/`useFetch` (gọi API, khỏi axios).

Code build dần trong `finance-tracker/frontend/`. Backend chạy sẵn tại `http://localhost:8000`, CORS đã mở cho `localhost:3000`.

## Lộ trình

| # | File | Build được gì | Khái niệm chính |
|---|------|----------------|------------------|
| 0 | [00-tong-quan.md](00-tong-quan.md) | Mental model + chuẩn bị | Nuxt là gì, bản đồ khái niệm ↔ Java/Laravel |
| 1 | [01-khoi-tao-va-cau-truc.md](01-khoi-tao-va-cau-truc.md) | App chạy, trang chào | Setup, cấu trúc thư mục, auto-import |
| 2 | [02-layout-routing.md](02-layout-routing.md) | Sidebar + 3 trang | File-based routing, layout, `NuxtLink`, `v-for` |
| 3 | [03-ket-noi-api.md](03-ket-noi-api.md) | Hiện category thật | `useFetch`/`$fetch`, runtimeConfig, types, lớp API |
| 4 | [04-categories-crud.md](04-categories-crud.md) | CRUD category | Reactivity, `v-model`, form, modal, `@click`, slot |
| 5 | [05-transactions-crud.md](05-transactions-crud.md) | Bảng + filter + phân trang | `watch`, query params, props/emit, component con |
| 6 | [06-state-pinia.md](06-state-pinia.md) | State dùng chung | Pinia store, `storeToRefs` |
| 7 | [07-reports-dashboard.md](07-reports-dashboard.md) | Dashboard + biểu đồ | `Promise.all`, `useAsyncData`, chart client-only |
| 8 | [08-hoan-thien-deploy.md](08-hoan-thien-deploy.md) | Polish + build + deploy | Error/toast, `nuxt build`, SSR vs SPA, env config |

## Bắt đầu

Đọc [00-tong-quan.md](00-tong-quan.md) trước → làm theo checklist chuẩn bị → sang phase 1.

> Mẹo học: đừng đọc hết một lượt rồi mới code. Mở 1 phase, **vừa đọc vừa gõ vừa chạy thử**. Khái niệm chỉ ngấm khi tay bạn gõ và mắt thấy nó chạy.
