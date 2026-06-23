# 01 — Khởi tạo project & hiểu cấu trúc Nuxt

> **Mục tiêu phase này:** Có 1 app Nuxt chạy được trong `finance-tracker/frontend/`, hiểu mỗi thư mục để làm gì, và thấy "auto-import" hoạt động.
> Cuối phase: mở `http://localhost:3000` thấy trang chào của mình.

---

## 1. Khái niệm trước khi gõ lệnh

### npm / npx là gì?
- `npm` = trình quản lý package của JS. **Tương đương Maven/Gradle**. File `package.json` ≈ `pom.xml`/`build.gradle`. `node_modules/` ≈ thư mục `.m2` nhưng nằm ngay trong project.
- `npx` = chạy 1 package mà không cần cài global trước (tải tạm rồi chạy). Dùng để scaffold project.

### Vì sao có `package.json` và `package-lock.json`?
- `package.json` = khai báo dependency bạn muốn (giống `pom.xml`).
- `package-lock.json` = khóa version chính xác đã cài (giống `uv.lock` bên Python, hay Gradle lockfile). **Commit cả 2 file.**

---

## 2. ✅ Các bước khởi tạo

> Chạy ở thư mục `finance-tracker/` (cùng cấp với `app/`).

```bash
# 1. Tạo app Nuxt tên "frontend". Scaffolder sẽ hỏi vài lựa chọn:
#    - package manager: chọn npm (cho đơn giản lúc học)
#    - TypeScript: YES
#    - Git: tùy (repo đã có .git ở finance-tracker rồi, có thể chọn No)
npm create nuxt@latest frontend

cd frontend

# 2. Cài Nuxt UI (bộ component). Lệnh nuxi tự thêm module vào nuxt.config.
npx nuxi module add ui

# 3. Chạy dev server
npm run dev
```

Mở `http://localhost:3000` → thấy trang mặc định của Nuxt. Server chạy ở chế độ **hot reload**: sửa file → trình duyệt tự cập nhật (giống Spring DevTools nhưng nhanh & mượt hơn nhiều).

> ⚠️ Nếu port 3000 bận: Nuxt nhảy sang 3001. Nhưng CORS backend chỉ mở 3000 (và 5173). Nên giữ 3000. Nếu kẹt, đóng app đang chiếm port hoặc chạy `npm run dev -- --port 3000`.

---

## 3. Tour cấu trúc thư mục (phần quan trọng nhất phase này)

Sau khi tạo, project trông như này (lược bớt):

```
frontend/
├─ nuxt.config.ts      # Cấu hình toàn app — "application.yml" của Nuxt
├─ app.vue             # Component gốc, bao quanh mọi trang — "layout root"
├─ package.json        # Dependencies — "pom.xml"
├─ tsconfig.json       # Cấu hình TypeScript
├─ public/             # File tĩnh phục vụ nguyên si (favicon, ảnh) — "src/main/resources/static"
└─ (các thư mục bạn sẽ TỰ tạo khi cần:)
   ├─ pages/           # Mỗi file = 1 route (Phase 02)
   ├─ layouts/         # Khung dùng lại cho nhiều trang (Phase 02)
   ├─ components/      # Component tái sử dụng — auto-import
   ├─ composables/     # Logic tái sử dụng (useXxx) — "@Service" (Phase 03)
   ├─ stores/          # Pinia store (Phase 06)
   ├─ types/           # Định nghĩa TypeScript type (Phase 03)
   └─ assets/          # CSS/ảnh cần build xử lý
```

> 📌 Khác Spring/Laravel: nhiều thư mục **không tồn tại sẵn**. Nuxt theo convention "có file mới có thư mục". Bạn tạo `pages/` thì Nuxt tự bật routing. Đây là điểm "magic" cần làm quen — không có file XML khai báo, **vị trí file CHÍNH LÀ khai báo**.

### `app.vue` — đọc thử
Mở `app.vue`. Cấu trúc 1 file `.vue` luôn gồm tối đa 3 khối:

```vue
<script setup lang="ts">
// Phần logic — chạy bằng TypeScript. Giống phần "controller" của component.
</script>

<template>
  <!-- Phần HTML hiển thị -->
</template>

<style scoped>
/* CSS chỉ áp dụng cho component này (scoped) */
</style>
```

So sánh: 1 file `.vue` = gộp 3 thứ mà bên Spring MVC bạn tách ra (Controller logic + JSP/Thymeleaf view + CSS). Gói chung 1 chỗ → dễ đọc theo tính năng.

`<script setup>` là cú pháp hiện đại của Vue 3: code khai báo ở top-level tự động "expose" ra template. Không cần `return { ... }` như kiểu cũ.

---

## 4. ✅ Việc thực hành: trang chào của mình

Sửa `app.vue` thành:

```vue
<script setup lang="ts">
const appName = 'Finance Tracker'
const today = new Date().toLocaleDateString('vi-VN')
</script>

<template>
  <UApp>
    <UContainer class="py-10">
      <h1 class="text-2xl font-bold">{{ appName }}</h1>
      <p class="text-gray-500">Hôm nay: {{ today }}</p>
      <UButton class="mt-4" icon="i-lucide-rocket">Bắt đầu thôi</UButton>
    </UContainer>
  </UApp>
</template>
```

Quan sát & hiểu:
- `{{ appName }}` = **interpolation**, nhúng biến JS vào HTML. Giống `${appName}` trong Thymeleaf / `{{ $appName }}` trong Blade.
- `UApp`, `UContainer`, `UButton` = component của **Nuxt UI**. Bạn **không hề import** chúng — đó là **auto-import**. Nuxt quét và tự nạp. (Giống `@ComponentScan` tự tìm bean, nhưng cho component UI.)
- `icon="i-lucide-rocket"` = Nuxt UI tích hợp sẵn bộ icon. Đổi tên icon thử xem.
- `class="..."` = Tailwind CSS (utility class). `py-10` = padding trên dưới, `text-2xl` = cỡ chữ. Không cần viết CSS riêng. (Sẽ quen dần, không cần học hết Tailwind ngay.)

> 💡 `UApp` nên là component bọc ngoài cùng — nó cung cấp context cho toast, modal... của Nuxt UI. Cứ giữ nó ở `app.vue`.

Lưu file → trình duyệt tự đổi. Đó là hot reload.

---

## 5. 🧠 Tự kiểm tra (trả lời được mới sang phase sau)

1. `node_modules/` tương đương cái gì bên Java? Có nên commit không? (Gợi ý: không — đã có trong `.gitignore`.)
2. 3 khối trong file `.vue` là gì, mỗi khối lo việc gì?
3. "Auto-import" nghĩa là gì? Tại sao mình dùng được `UButton` mà không viết dòng `import`?
4. Muốn thêm 1 route mới thì mình tạo gì, ở đâu? (Trả lời được câu này tức là đã nắm tinh thần phase 02.)
5. `{{ }}` dùng để làm gì trong template?

---

## 6. Kết quả mong đợi

- [ ] `finance-tracker/frontend/` tồn tại, `npm run dev` chạy không lỗi.
- [ ] `http://localhost:3000` hiện trang chào có tên app + nút.
- [ ] Hiểu sơ đồ thư mục và vai trò `nuxt.config.ts`, `app.vue`, `package.json`.

→ Tiếp: [`02-layout-routing.md`](02-layout-routing.md) — dựng khung app và điều hướng nhiều trang.
