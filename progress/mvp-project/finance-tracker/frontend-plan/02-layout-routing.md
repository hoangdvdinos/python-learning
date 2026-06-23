# 02 — Layout & Routing (khung app + điều hướng)

> **Mục tiêu phase này:** Dựng khung app có sidebar điều hướng giữa 3 trang: Dashboard, Transactions, Categories. Hiểu **file-based routing** và **layout**.
> Cuối phase: bấm menu chuyển qua lại 3 trang (nội dung tạm là placeholder).

---

## 1. File-based routing — "tên file là route"

Trong Nuxt, bạn **không khai báo route bằng tay**. Tạo file trong `pages/` → Nuxt tự sinh route.

| File tạo ra | URL | So với Spring | So với Laravel |
|-------------|-----|---------------|-----------------|
| `pages/index.vue` | `/` | `@GetMapping("/")` | `Route::get('/')` |
| `pages/transactions.vue` | `/transactions` | `@GetMapping("/transactions")` | `Route::get('/transactions')` |
| `pages/categories.vue` | `/categories` | `@GetMapping("/categories")` | ... |
| `pages/transactions/[id].vue` | `/transactions/123` | `@GetMapping("/transactions/{id}")` | `{id}` route param |

> 📌 Điểm "magic" lớn nhất khi từ Spring sang: **không có file route trung tâm**. Cấu trúc thư mục `pages/` CHÍNH LÀ bảng route. Thêm file = thêm endpoint, xóa file = xóa route.

⚠️ Khoảnh khắc bật routing: ngay khi bạn tạo thư mục `pages/` và có ít nhất 1 file trong đó, Nuxt **ngừng** dùng `app.vue` làm nội dung trực tiếp và bắt đầu render trang theo URL. Lúc đó `app.vue` phải chứa `<NuxtPage />` (xem mục 3).

---

## 2. ✅ Tạo 3 trang placeholder

Tạo các file:

`pages/index.vue` (Dashboard):
```vue
<script setup lang="ts">
// chưa có gì, sẽ build ở Phase 07
</script>

<template>
  <div>
    <h1 class="text-xl font-bold mb-4">Dashboard</h1>
    <p class="text-gray-500">Sẽ có thẻ số liệu + biểu đồ ở Phase 07.</p>
  </div>
</template>
```

`pages/transactions.vue` và `pages/categories.vue`: copy tương tự, đổi tiêu đề.

---

## 3. `app.vue` + `<NuxtPage />` + `<NuxtLink>`

Sửa `app.vue` để làm "khung gốc" có chỗ render trang:

```vue
<template>
  <UApp>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </UApp>
</template>
```

- `<NuxtPage />` = **chỗ thay nội dung theo URL**. Giống `<router-view>` / vùng `@yield('content')` trong Blade / `<th:block layout:fragment>` của Thymeleaf. URL đổi → Nuxt nhét trang tương ứng vào đây.
- `<NuxtLayout />` = bọc layout (định nghĩa ở mục 4).

---

## 4. Layout — khung dùng chung (sidebar + header)

Trang nào cũng cần sidebar + header → tách ra **layout** để khỏi lặp. Giống `layouts/app.blade.php` (Laravel) hay layout template Thymeleaf.

Tạo `layouts/default.vue`:

```vue
<script setup lang="ts">
// Mỗi link: nhãn + đường dẫn + icon
const links = [
  { label: 'Dashboard', to: '/', icon: 'i-lucide-layout-dashboard' },
  { label: 'Giao dịch', to: '/transactions', icon: 'i-lucide-arrow-left-right' },
  { label: 'Danh mục', to: '/categories', icon: 'i-lucide-tags' },
]
</script>

<template>
  <div class="min-h-screen flex">
    <!-- Sidebar -->
    <aside class="w-60 border-r p-4 space-y-1">
      <div class="font-bold text-lg mb-4">💰 Finance</div>
      <NuxtLink
        v-for="link in links"
        :key="link.to"
        :to="link.to"
        class="flex items-center gap-2 px-3 py-2 rounded hover:bg-gray-100"
        active-class="bg-gray-200 font-medium"
      >
        <UIcon :name="link.icon" />
        {{ link.label }}
      </NuxtLink>
    </aside>

    <!-- Vùng nội dung: slot nhận nội dung trang -->
    <main class="flex-1 p-8">
      <slot />
    </main>
  </div>
</template>
```

Khái niệm mới xuất hiện ở đây — **đọc kỹ**:

- **`v-for`** = vòng lặp render. `v-for="link in links"` ≈ `<th:block th:each="link : ${links}">` (Thymeleaf) / `@foreach` (Blade). Render 1 `NuxtLink` cho mỗi phần tử mảng.
- **`:key`** = mỗi item lặp cần key duy nhất để Vue tối ưu re-render. (Bắt buộc khi `v-for`.)
- **`:to="link.to"`** — dấu `:` phía trước = **binding động**. `to="/"` là chuỗi cố định; `:to="link.to"` là "lấy giá trị từ biến JS". Đây là cú pháp `v-bind`. Nhớ: **có `:` = giá trị là biểu thức JS, không có `:` = chuỗi literal.**
- **`<NuxtLink>`** = link điều hướng nội bộ. Khác thẻ `<a>` thường: nó chuyển trang **không reload toàn trang** (SPA navigation) — nhanh, mượt. `active-class` tự gắn class khi link đang active. (Giống `routerLink` của Angular.)
- **`<slot />`** = "chỗ nhét nội dung con vào". Layout là cái khung, `<slot />` là lỗ hổng để nội dung trang điền vào. Tương đương `@yield('content')` / `layout:fragment`.

> File layout tên `default.vue` được Nuxt dùng **mặc định** cho mọi trang. Muốn trang khác layout thì tạo layout khác + khai báo trong trang đó. Giờ chưa cần.

---

## 5. Thử nghiệm để hiểu

1. Bấm qua lại 3 menu — chú ý **URL đổi mà trang KHÔNG chớp trắng (không reload)**. Đó là client-side routing.
2. Mở DevTools (F12) → tab Network → bấm menu. Thấy **không có request HTML mới** mỗi lần chuyển. So với multi-page app truyền thống (mỗi click = 1 request server) → đây là khác biệt cốt lõi của SPA.
3. Gõ thẳng `http://localhost:3000/categories` vào address bar rồi Enter → lần này CÓ load (vào thẳng route). Sau đó bấm menu thì lại không reload nữa.

---

## 6. 🧠 Tự kiểm tra

1. Muốn thêm trang `/settings` thì làm gì? (1 thao tác duy nhất.)
2. `<NuxtPage />` và `<slot />` khác nhau chỗ nào? (Gợi ý: 1 cái cho router, 1 cái cho layout.)
3. `:to="..."` và `to="..."` khác nhau ra sao? Khi nào dùng cái nào?
4. Vì sao `v-for` bắt buộc có `:key`?
5. Vì sao bấm `<NuxtLink>` không reload trang, mà gõ URL vào browser thì có?

---

## 7. Kết quả mong đợi

- [ ] Có `pages/index.vue`, `pages/transactions.vue`, `pages/categories.vue`.
- [ ] Có `layouts/default.vue` với sidebar.
- [ ] Bấm menu chuyển trang mượt, link active sáng lên.

→ Tiếp: [`03-ket-noi-api.md`](03-ket-noi-api.md) — kéo dữ liệu thật từ backend FastAPI về.
