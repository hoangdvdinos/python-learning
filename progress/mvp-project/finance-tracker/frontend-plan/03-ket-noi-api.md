# 03 — Kết nối API (kéo dữ liệu thật từ backend)

> **Mục tiêu phase này:** Trang Categories hiển thị danh sách category **thật** lấy từ FastAPI. Hiểu `useFetch`/`$fetch`, cấu hình base URL, định nghĩa TypeScript type khớp schema backend, và tách 1 "lớp API" (giống service/repository).
> Cuối phase: vào `/categories` thấy danh sách category từ DB hiện ra.

---

## 1. Cấu hình base URL của API (`runtimeConfig`)

Không hardcode `http://localhost:8000` rải rác khắp nơi. Khai báo 1 chỗ — giống `application.yml` + `@Value`, hoặc `.env` + `config()` của Laravel.

Sửa `nuxt.config.ts`:

```ts
export default defineNuxtConfig({
  modules: ['@nuxt/ui'],

  runtimeConfig: {
    // public = client (trình duyệt) đọc được. Để private thì bỏ ngoài "public".
    public: {
      apiBase: 'http://localhost:8000/api/v1',
    },
  },
})
```

> Có thể override bằng biến môi trường: đặt `NUXT_PUBLIC_API_BASE=...` thì Nuxt tự đọc đè lên. (Quy tắc: `NUXT_` + tên key viết hoa.) Giống đọc env trong Spring Boot.

Lấy ra trong code:
```ts
const config = useRuntimeConfig()
const base = config.public.apiBase  // "http://localhost:8000/api/v1"
```

---

## 2. Định nghĩa type khớp với schema backend (TypeScript)

Backend trả JSON theo schema Pydantic. Bên frontend ta khai báo `interface` để có **type safety như Java** — IDE gợi ý, bắt lỗi gõ sai tên field.

Tạo `types/index.ts`:

```ts
// Khớp với CategoryResponse (app/schemas/category.py)
export interface Category {
  id: number
  name: string
  type: 'income' | 'expense'   // union type ~ enum của Java
  icon: string | null
  color: string | null
}

// Khớp với TransactionResponse
export interface Transaction {
  id: number
  amount: string               // Decimal serialize thành chuỗi JSON -> giữ string cho an toàn
  type: string
  description: string | null
  transaction_date: string     // date ISO "2026-06-23"
  category_id: number
  category: Category
}

// Khớp với SummaryResponse
export interface Summary {
  total_income: string
  total_expense: string
  balance: string
}
```

> 📌 Dân Java hay vấp: `interface` của TS chỉ tồn tại **lúc compile** để check, **không** sinh ra code runtime, và **không tự validate** JSON như Pydantic. Nó chỉ là "lời hứa về hình dạng dữ liệu". Backend mới là nơi validate thật.
>
> 📌 `amount` để `string` vì backend dùng `Decimal` → serialize ra JSON thành chuỗi (`"150000.00"`) để khỏi mất chính xác. Khi cần hiển thị/tính, parse `Number(amount)`. (Giống lý do bên Java dùng `BigDecimal` cho tiền, không dùng `double`.)

---

## 3. `$fetch` vs `useFetch` — phân biệt cho rõ (rất hay nhầm)

Nuxt có sẵn 2 cách gọi HTTP, **không cần axios**:

| | `useFetch(url)` | `$fetch(url)` |
|---|------------------|----------------|
| Bản chất | Composable bọc quanh `$fetch`, có sẵn state | Hàm gọi HTTP thuần |
| Trả về | `{ data, status, error, refresh }` (reactive) | Promise dữ liệu (`await` ra luôn) |
| Dùng khi | **Lấy data để render trang** (lúc setup component) | **Hành động** do user kích hoạt: submit form, click xóa |
| Tương tự Java | — | `restTemplate.getForObject(...)` / `await webClient...` |

Quy tắc ngón tay cái:
- **Tải dữ liệu hiển thị** → `useFetch` (nó lo loading/error/SSR giúp bạn).
- **Tạo / sửa / xóa khi user bấm nút** → `$fetch` bên trong 1 hàm `async`.

> ⚠️ Đừng gọi `useFetch` bên trong hàm xử lý sự kiện (vd `onClick`). `useFetch` phải gọi ở top-level của `<script setup>`. Trong event handler thì dùng `$fetch`. Nhớ kỹ điều này để khỏi lỗi khó hiểu.

---

## 4. Tách "lớp API" thành composable (giống Repository/Service)

Thay vì rải URL khắp component, gom lời gọi API vào 1 chỗ — đúng tinh thần **Repository pattern** mà backend đang dùng (`category_repo.py`).

Tạo `composables/useApi.ts`:

```ts
import type { Category } from '~/types'

// Composable: hàm bắt đầu bằng "use", Nuxt AUTO-IMPORT (khỏi import thủ công).
export function useApi() {
  const config = useRuntimeConfig()
  const base = config.public.apiBase

  return {
    categories: {
      list: (type?: 'income' | 'expense') =>
        $fetch<Category[]>(`${base}/categories`, { query: { type } }),

      create: (body: Partial<Category>) =>
        $fetch<Category>(`${base}/categories`, { method: 'POST', body }),

      update: (id: number, body: Partial<Category>) =>
        $fetch<Category>(`${base}/categories/${id}`, { method: 'PATCH', body }),

      remove: (id: number) =>
        $fetch(`${base}/categories/${id}`, { method: 'DELETE' }),
    },
  }
}
```

Giải thích cho dân Java:
- `useApi()` = factory trả về 1 object có các method gọi API. Như 1 `@Service` gói các call.
- `$fetch<Category[]>(...)` — phần `<Category[]>` là **generic**, y hệt `List<Category>` của Java: bảo TS "kết quả có kiểu này".
- `{ query: { type } }` → Nuxt tự ghép thành `?type=income`. Nếu `type` là `undefined` thì bỏ qua (đúng ý backend: filter optional).
- `Partial<Category>` = "object có MỘT SỐ field của Category" (dùng cho create/update). Tiện cho PATCH.
- Đặt file trong `composables/` + tên `useApi` → **auto-import**, component xài thẳng `useApi()` không cần `import`.

---

## 5. ✅ Hiển thị danh sách category thật

Sửa `pages/categories.vue`:

```vue
<script setup lang="ts">
const api = useApi()

// useFetch để TẢI dữ liệu render. data/pending/error đều reactive.
const { data: categories, pending, error, refresh } = await useFetch(
  () => api.categories.list(),   // hàm trả promise
  { key: 'categories' }          // key cache, tránh trùng
)
</script>

<template>
  <div>
    <h1 class="text-xl font-bold mb-4">Danh mục</h1>

    <p v-if="pending">Đang tải...</p>
    <p v-else-if="error" class="text-red-500">Lỗi tải dữ liệu 😢</p>

    <ul v-else class="space-y-2">
      <li
        v-for="cat in categories"
        :key="cat.id"
        class="flex items-center gap-2 border rounded p-2"
      >
        <span :style="{ color: cat.color ?? '#888' }">{{ cat.icon ?? '•' }}</span>
        <span>{{ cat.name }}</span>
        <UBadge :color="cat.type === 'income' ? 'success' : 'error'">
          {{ cat.type }}
        </UBadge>
      </li>
    </ul>
  </div>
</template>
```

Khái niệm mới:
- **`v-if` / `v-else-if` / `v-else`** = render có điều kiện. Giống `th:if` (Thymeleaf) / `@if` (Blade). Ở đây xử lý 3 trạng thái: đang tải / lỗi / có data — pattern cực hay gặp.
- **`pending`** = `true` khi đang chờ response. Khỏi tự quản lý cờ loading — `useFetch` cho sẵn.
- **`cat.color ?? '#888'`** = **nullish coalescing**: nếu `color` là `null`/`undefined` thì lấy `'#888'`. Giống `Optional.orElse(...)` của Java.
- **`:style="{ color: ... }"`** = bind style động bằng object.
- `refresh()` = gọi lại API để tải mới (dùng ở Phase 04 sau khi thêm/xóa).

> Nếu thấy lỗi CORS trong Console: kiểm tra backend đang chạy và frontend ở đúng `localhost:3000`. CORS backend đã whitelist port này rồi.

---

## 6. 🧠 Tự kiểm tra

1. Khi nào dùng `useFetch`, khi nào dùng `$fetch`? Cho 1 ví dụ mỗi loại trong app này.
2. `interface Category` ở frontend có **validate** dữ liệu trả về không? Nếu backend trả thiếu field thì sao?
3. Vì sao đặt base URL trong `runtimeConfig` thay vì gõ thẳng trong từng component?
4. `$fetch<Category[]>` — phần `<Category[]>` đóng vai trò gì? Tương ứng cú pháp nào bên Java?
5. Vì sao file `composables/useApi.ts` dùng được mà không cần `import useApi`?
6. `cat.color ?? '#888'` chạy ra gì khi `color` = `null`? Khi `color` = `'#FF0000'`?

---

## 7. Kết quả mong đợi

- [ ] `runtimeConfig.public.apiBase` đã cấu hình.
- [ ] `types/index.ts` có `Category`, `Transaction`, `Summary`.
- [ ] `composables/useApi.ts` gom các call category.
- [ ] `/categories` hiển thị danh sách thật, có trạng thái loading & error.

→ Tiếp: [`04-categories-crud.md`](04-categories-crud.md) — thêm/sửa/xóa category, học reactivity và form.
