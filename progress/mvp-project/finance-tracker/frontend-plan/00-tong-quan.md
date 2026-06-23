# 00 — Tổng quan & Bản đồ học tập

> Mục tiêu của cả series này: **vừa build frontend Nuxt cho Finance Tracker, vừa hiểu Nuxt từ gốc**.
> Mỗi file là 1 phase. Làm xong phase nào là có thứ chạy được + hiểu khái niệm mới của phase đó.

---

## 1. Ta đang build cái gì?

Backend `finance-tracker` (FastAPI) đã chạy sẵn tại `http://localhost:8000`, expose REST API:

| Nhóm | Endpoint | Việc |
|------|----------|------|
| Categories | `/api/v1/categories` | CRUD danh mục thu/chi (có icon, color) |
| Transactions | `/api/v1/transactions` | CRUD giao dịch, có filter + phân trang |
| Reports | `/api/v1/reports/{summary,monthly,by-category}` | Tổng hợp số liệu cho dashboard |

Không có auth, single-user. CORS backend **đã mở sẵn** cho `http://localhost:3000` — đúng port mặc định của Nuxt dev. Nghĩa là không cần đụng gì backend, cứ thế gọi.

Frontend ta sẽ build gồm 4 màn:
1. **Dashboard** — thẻ tổng thu/chi/số dư + biểu đồ.
2. **Transactions** — bảng giao dịch, filter, phân trang, thêm/sửa/xóa.
3. **Categories** — quản lý danh mục.
4. **Layout chung** — sidebar/header điều hướng giữa các màn.

---

## 2. Nuxt là gì, và tại sao không dùng Vue trần?

**Vue** = thư viện UI (component, reactivity). Giống như... chỉ có Servlet API trần.

**Nuxt** = framework bọc quanh Vue, lo sẵn routing, cấu trúc thư mục, build, SSR, auto-import... Giống **Spring Boot bọc quanh Servlet/Spring core**, hoặc **Laravel bọc quanh PHP**: bạn theo convention, framework lo phần boilerplate.

> 📌 Mental model cho dân Java/Laravel:
> - Vue ↔ Spring core / PHP thuần
> - Nuxt ↔ Spring Boot / Laravel (convention over configuration)

Vì bạn mới học, **đừng học Vue trần trước rồi mới sang Nuxt**. Học thẳng Nuxt, khái niệm Vue (reactivity, component) sẽ ngấm dần qua từng phase.

---

## 3. Bản đồ khái niệm: Nuxt/Vue ↔ thứ bạn đã biết

Bảng này là "từ điển dịch" — quay lại tra khi gặp khái niệm lạ.

| Khái niệm Nuxt/Vue | Tương đương bên Java/Spring | Tương đương Laravel | Ghi chú |
|--------------------|------------------------------|----------------------|---------|
| File-based routing (`pages/`) | `@RequestMapping` nhưng tự suy từ tên file | `routes/web.php` | Tạo file = tạo route, không khai báo tay |
| `app.vue` / `layouts/` | Layout template chung (sitemesh / thymeleaf layout) | Blade `layouts/app.blade.php` | Khung bao quanh mọi trang |
| Component (`.vue`) | — (gần nhất: JSP fragment / tag file) | Blade component | 1 file = template + logic + style |
| `ref` / `reactive` | Field của bean, nhưng "có observer" | — | Biến mà khi đổi → UI tự render lại |
| `computed` | Getter dẫn xuất (derived) | Accessor | Tự tính lại khi dependency đổi |
| Composable (`useXxx`) | `@Service` / bean tái sử dụng logic | Service class / helper | Hàm gom logic tái dùng, KHÔNG phải UI |
| `useFetch` / `$fetch` | `RestTemplate` / `WebClient` / Feign | `Http::get()` | Gọi HTTP tới backend |
| Pinia store | Spring singleton bean giữ state | Singleton service / session | State dùng chung toàn app |
| `runtimeConfig` | `application.yml` + `@Value` | `.env` + `config()` | Cấu hình (vd base URL của API) |
| Auto-import | Component scan / `@ComponentScan` | Service container auto-resolve | Nuxt tự import component & composable |
| `nuxt build` / `generate` | `mvn package` → jar | `npm run build` | Đóng gói để deploy |

Điểm "dễ vấp" với người từ Java sang (ghi nhớ sớm):
- **JS không có kiểu tĩnh mặc định** → ta dùng **TypeScript** để có cảm giác như Java (interface, type). Phase 03 sẽ định nghĩa type khớp với schema Pydantic của backend.
- **Reactivity ≠ field thường**: gán `x = 5` chưa chắc UI update; phải qua `ref`. Sẽ giải thích kỹ ở Phase 04.
- **`==` lỏng lẻo trong JS** → luôn dùng `===` (giống ý thức `equals()` vs `==` bên Java, nhưng ngược đời hơn).
- **`null` vs `undefined`**: JS có 2 loại "rỗng". Backend trả `null`, JS hay gặp `undefined`. Quen dần.

---

## 4. Tech stack đã chốt

| Thành phần | Chọn | Vai trò |
|-----------|------|---------|
| Framework | **Nuxt** (bản mới nhất) | Khung frontend |
| Ngôn ngữ | **TypeScript** | Type-safe như Java |
| UI components | **Nuxt UI** | Bộ component dựng sẵn (button, table, modal, form) + Tailwind có sẵn |
| State | **Pinia** | Store dùng chung (Phase 06) |
| Charts | **Chart.js** (qua `vue-chartjs`) hoặc Nuxt UI chart | Biểu đồ dashboard (Phase 07) |
| Gọi API | `$fetch` / `useFetch` (built-in Nuxt) | Không cần axios |

> Chọn **Nuxt UI** nghĩa là: không tự code button/modal/table từ đầu. Đổi lại học nhanh, màn hình đẹp ngay. Ta vẫn hiểu Vue/Nuxt core vì phần *logic* (state, fetch, routing) tự viết hết.

---

## 5. Roadmap các phase

| Phase | File | Build được gì | Khái niệm mới học |
|-------|------|----------------|--------------------|
| 0 | `00-tong-quan.md` | (đang đọc) | Mental model tổng thể |
| 1 | `01-khoi-tao-va-cau-truc.md` | App Nuxt chạy được, trang "Hello" | Cài đặt, cấu trúc thư mục, auto-import |
| 2 | `02-layout-routing.md` | Khung app: sidebar + 3 trang điều hướng | File-based routing, layout, `NuxtLink` |
| 3 | `03-ket-noi-api.md` | Hiện danh sách category thật từ backend | `useFetch`, `runtimeConfig`, TypeScript types, lớp API |
| 4 | `04-categories-crud.md` | CRUD category đầy đủ (form + modal) | Reactivity (`ref`/`computed`), `v-model`, form, sự kiện |
| 5 | `05-transactions-crud.md` | Bảng giao dịch + filter + phân trang | Query params, `watch`, component con, props/emit |
| 6 | `06-state-pinia.md` | Refactor chia sẻ state category toàn app | Pinia store, vì sao cần global state |
| 7 | `07-reports-dashboard.md` | Dashboard: thẻ số liệu + biểu đồ | Tích hợp chart, `computed` nâng cao, gọi nhiều API |
| 8 | `08-hoan-thien-deploy.md` | Loading/error/toast + build production | Xử lý lỗi, `nuxt build`, deploy |

**Cách dùng plan:** Làm tuần tự. Mỗi phase có phần **"✅ Checklist"** (việc cần làm) và **"🧠 Tự kiểm tra"** (câu hỏi để chắc là đã hiểu, không chỉ copy code). Đừng nhảy phase — mỗi phase build lên phase trước.

---

## 6. Chuẩn bị trước khi bắt đầu Phase 1

- [ ] Cài **Node.js** bản LTS (≥ 20). Kiểm tra: `node -v`, `npm -v`. (Node = "JRE" của thế giới JS; npm = "Maven/Gradle".)
- [ ] Backend chạy được: `uv run uvicorn app.main:app --reload` → mở `http://localhost:8000/docs` thấy Swagger.
- [ ] Chạy `seed.py` để có dữ liệu mẫu (nếu chưa): `uv run python seed.py`.
- [ ] Editor: VS Code + extension **Vue (Official)** (tên cũ Volar) để có autocomplete `.vue`.

Xong các gạch đầu dòng trên → sang [`01-khoi-tao-va-cau-truc.md`](01-khoi-tao-va-cau-truc.md).
