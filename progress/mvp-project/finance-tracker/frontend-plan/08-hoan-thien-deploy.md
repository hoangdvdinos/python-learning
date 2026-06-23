# 08 — Hoàn thiện & Deploy

> **Mục tiêu phase này:** Đánh bóng trải nghiệm (loading, error, toast xác nhận), hiểu `nuxt build` / cách đóng gói, và deploy thử. Sau phase này bạn có 1 app hoàn chỉnh + hiểu vòng đời từ dev tới production.

---

## 1. Loading & error states tử tế

Cho tới giờ ta xử lý loading/error khá thô (`v-if="pending"`). Chuẩn hóa lại:

- **Loading**: dùng `USkeleton` của Nuxt UI để hiện khung xám nhấp nháy thay vì chữ "Đang tải".
- **Error**: `useFetch` trả `error`; hiện `UAlert` đỏ + nút "Thử lại" gọi `refresh()`.

```vue
<USkeleton v-if="pending" class="h-10 w-full" />
<UAlert v-else-if="error" color="error" title="Không tải được dữ liệu">
  <template #actions><UButton @click="refresh">Thử lại</UButton></template>
</UAlert>
<div v-else><!-- nội dung --></div>
```

---

## 2. Toast thông báo (thay `alert`/`confirm`)

Nuxt UI có `useToast()` — thông báo góc màn hình thay cho `alert()` xấu xí.

```ts
const toast = useToast()

async function save() {
  try {
    await store.create({ ...form })
    toast.add({ title: 'Đã lưu danh mục', color: 'success' })
    open.value = false
  } catch (e) {
    toast.add({ title: 'Lưu thất bại', description: String(e), color: 'error' })
  }
}
```

> 📌 **`try/catch`** ở đây giống hệt Java: bọc lời gọi có thể ném lỗi (HTTP 4xx/5xx → `$fetch` ném exception), bắt lại để báo người dùng. Backend của bạn trả lỗi dạng `{ error_code, message }` (xem `app/main.py`) — có thể đọc `e.data` để lấy `message` chi tiết và hiện cho đẹp.
> `useToast()` cần `<UApp>` bọc ngoài (đã có ở `app.vue` từ Phase 01).

Xác nhận xóa: thay `confirm()` bằng `UModal` xác nhận hoặc `UPopover`. Tùy chọn — không bắt buộc cho bản học.

---

## 3. Một vài "polish" đáng làm

- **Format ngày/tiền tập trung**: gom `money()`, `formatDate()` vào `composables/useFormat.ts` để khỏi lặp ở mỗi component (DRY — như utility class bên Java).
- **Empty state**: khi list rỗng, hiện hình/chữ thân thiện thay vì khoảng trắng.
- **Tiêu đề trang**: dùng `useHead({ title: 'Giao dịch · Finance' })` trong mỗi page để đổi tiêu đề tab trình duyệt.
- **Dark mode**: Nuxt UI hỗ trợ sẵn; thêm nút `UButton` gọi `useColorMode()` để bật/tắt. (Tùy hứng.)

---

## 4. Build production — hiểu chuyện gì xảy ra

Trong dev, `npm run dev` chạy server có hot reload. Lên production thì khác:

```bash
npm run build      # đóng gói toàn app -> thư mục .output/
node .output/server/index.mjs   # chạy server Node production
```

- `nuxt build` = biên dịch + minify + tách code, tạo `.output/`. **Tương đương `mvn package` ra file jar.** Kết quả là 1 Node server (có cả phần SSR).
- `.output/` là thứ đem đi deploy (không đem `node_modules` hay source).

Hai kiểu deploy Nuxt — hiểu để chọn:
| Kiểu | Lệnh | Khi nào | Tương tự |
|------|------|---------|----------|
| **SSR / Node server** | `nuxt build` → chạy `.output/server` | Cần server-side rendering, SEO | Spring Boot jar chạy trên server |
| **SPA / Static** | đặt `ssr: false` rồi `nuxt generate` | App nội bộ, không cần SEO, host tĩnh | Bundle JS tĩnh đẩy lên CDN/nginx |

> Với app finance tracker nội bộ này, **SPA tĩnh là đủ và đơn giản nhất**: đặt `ssr: false` trong `nuxt.config.ts`, chạy `npm run generate`, lấy thư mục `.output/public/` đẩy lên bất kỳ static host nào (hoặc serve bằng nginx). Khi đó frontend chỉ là HTML+JS gọi thẳng API backend.

---

## 5. Cấu hình API URL cho production

Dev thì `apiBase = http://localhost:8000/...`. Production backend ở domain khác → **đừng sửa code**, dùng biến môi trường (đã chuẩn bị ở Phase 03):

```bash
# khi build/chạy production:
NUXT_PUBLIC_API_BASE=https://api.your-domain.com/api/v1 npm run build
```
Nuxt tự đọc `NUXT_PUBLIC_API_BASE` đè lên `runtimeConfig.public.apiBase`. (Đúng tinh thần tách config khỏi code — như `pydantic-settings` bạn đã dùng ở backend.)

> ⚠️ Nhớ cập nhật **CORS** ở backend (`app/main.py`, `allow_origins`) để thêm domain frontend production, nếu không trình duyệt sẽ chặn.

---

## 6. 🧠 Tự kiểm tra

1. `npm run dev` và `npm run build` khác nhau ra sao? Cái nào dùng để deploy?
2. Khi nào chọn SSR, khi nào chọn SPA tĩnh cho app này?
3. Để đổi API URL giữa dev và production mà không sửa code, ta làm thế nào?
4. `$fetch` khi backend trả lỗi 404/500 thì xảy ra gì trong JS? Bắt bằng cách nào?
5. Vì sao deploy production cần đụng lại CORS ở backend?

---

## 7. Kết quả mong đợi (cũng là tổng kết cả series)

- [ ] App có loading skeleton + error + toast tử tế.
- [ ] Build production thành công (`.output/`).
- [ ] Hiểu SSR vs SPA và cách cấu hình API URL theo môi trường.
- [ ] **Tự tin**: routing, layout, fetch, reactivity, form, props/emit, store, chart, build.

---

## 8. Đi tiếp từ đây (gợi ý nâng cao, không bắt buộc)

- Thêm **auth** (backend chưa có) — học `middleware/`, route guard của Nuxt.
- **Validation form** chặt hơn với Zod + `UForm` schema.
- **Optimistic update**: cập nhật UI trước, rollback nếu API lỗi.
- **Test**: Vitest + `@nuxt/test-utils`.
- Tách **monorepo** gọn hơn hoặc Docker hóa cả backend + frontend.

Chúc mừng — bạn vừa đi từ "chưa biết Nuxt" tới 1 app full CRUD + dashboard, và hiểu *vì sao* từng mảnh hoạt động chứ không chỉ copy. 🎉
