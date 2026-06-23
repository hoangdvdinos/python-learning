# 06 — State management với Pinia (chia sẻ state toàn app)

> **Mục tiêu phase này:** Hiểu **vì sao cần global state**, dùng **Pinia** để quản lý danh mục 1 chỗ duy nhất. Refactor để Categories + Transactions dùng chung store, hết fetch lặp.
> Đây là refactor, không thêm tính năng người dùng thấy — nhưng là kiến trúc quan trọng.

---

## 1. Vấn đề: state đang bị trùng lặp

Hiện tại cả `pages/categories.vue` và `pages/transactions.vue` đều tự `useFetch(() => api.categories.list())`. Tức là:
- Gọi API category **2 lần** ở 2 trang.
- Khi thêm category ở trang Categories, trang Transactions **không biết** → dropdown chọn category bị cũ.

Cần 1 **nguồn sự thật duy nhất** (single source of truth) cho danh mục, mọi trang đọc chung.

So sánh:
- Spring: 1 **singleton bean** giữ state, inject vào nhiều nơi.
- Đây: **Pinia store** = singleton sống suốt vòng đời app phía client, component nào cũng `use` được.

---

## 2. Cài & hiểu Pinia

```bash
npx nuxi module add pinia
```
(Lệnh này cài `@pinia/nuxt` và thêm vào `nuxt.config.ts`. Sau đó `defineStore` được **auto-import**.)

Một store gồm 3 phần — ánh xạ rất sạch sang Vue:
| Phần store | Là gì | Tương đương component |
|------------|-------|------------------------|
| `state` | dữ liệu | `ref`/`reactive` |
| `getters` | giá trị dẫn xuất | `computed` |
| `actions` | hàm thay đổi state (kể cả async, gọi API) | method |

---

## 3. ✅ Tạo store danh mục

Tạo `stores/categories.ts`:

```ts
import type { Category } from '~/types'

// "setup store" — viết y như <script setup>, trả ra cái cần expose.
export const useCategoriesStore = defineStore('categories', () => {
  const api = useApi()

  // --- state ---
  const items = ref<Category[]>([])
  const loaded = ref(false)

  // --- getters (computed) ---
  const incomeCategories = computed(() => items.value.filter(c => c.type === 'income'))
  const expenseCategories = computed(() => items.value.filter(c => c.type === 'expense'))

  // --- actions ---
  async function fetchAll(force = false) {
    if (loaded.value && !force) return   // đã có thì khỏi gọi lại
    items.value = await api.categories.list()
    loaded.value = true
  }

  async function create(body: Partial<Category>) {
    await api.categories.create(body)
    await fetchAll(true)   // refetch để mọi nơi cùng mới
  }

  async function update(id: number, body: Partial<Category>) {
    await api.categories.update(id, body)
    await fetchAll(true)
  }

  async function remove(id: number) {
    await api.categories.remove(id)
    await fetchAll(true)
  }

  return { items, loaded, incomeCategories, expenseCategories, fetchAll, create, update, remove }
})
```

> 📌 `defineStore('categories', ...)` — chuỗi `'categories'` là **id duy nhất** của store. Gọi `useCategoriesStore()` ở 10 component khác nhau đều trả về **cùng 1 instance** (singleton). Giống inject cùng 1 bean.

---

## 4. ✅ Refactor trang Categories dùng store

```vue
<script setup lang="ts">
const store = useCategoriesStore()

// đảm bảo đã tải. await để SSR/hydrate đúng.
await store.fetchAll()

// dùng storeToRefs để giữ reactivity khi destructure state/getters
const { items: categories } = storeToRefs(store)

// ... các hàm openCreate/openEdit/save như Phase 04, nhưng:
async function save() {
  if (editingId.value === null) await store.create({ ...form })
  else await store.update(editingId.value, { ...form })
  open.value = false
  // KHÔNG cần refresh() — store.create đã refetch, categories tự cập nhật
}
async function remove(id: number) {
  if (!confirm('Xóa danh mục này?')) return
  await store.remove(id)
}
</script>
```

> ⚠️ **Bẫy quan trọng:** đừng destructure thẳng `const { items } = store` — sẽ **mất reactivity** (lấy ra giá trị tĩnh). Phải dùng **`storeToRefs(store)`** cho state & getters. Còn **actions** (hàm) thì destructure thẳng được (`const { create } = store`). Nhớ kỹ: *state/getters → storeToRefs; actions → lấy thẳng.*

## 5. ✅ Trang Transactions dùng store cho dropdown category

```vue
<script setup lang="ts">
const store = useCategoriesStore()
await store.fetchAll()           // nếu trang khác đã tải, hàm này return ngay (loaded=true)
const { items: categories } = storeToRefs(store)
// ... dùng `categories` đổ vào USelect chọn danh mục
</script>
```

Giờ thử: thêm 1 category ở trang Categories → sang trang Transactions → dropdown **đã có** category mới. Vì cùng 1 store. Đây chính là lợi ích bạn vừa tạo ra.

---

## 6. Khi nào cần store, khi nào không? (đừng lạm dụng)

| Dùng store khi | Dùng state cục bộ (`ref` trong component) khi |
|----------------|-----------------------------------------------|
| Dữ liệu dùng ở **nhiều trang** (categories, user hiện tại...) | Dữ liệu chỉ của 1 trang (vd: modal đang mở hay không) |
| Cần đồng bộ khi 1 nơi đổi | Form tạm, filter cục bộ |
| "Single source of truth" | Trạng thái UI thoáng qua |

> Đừng nhét MỌI thứ vào store (sai lầm phổ biến). Categories hợp lý (toàn app dùng). Còn `open`/`editingId` của modal thì cứ để `ref` trong component. Quy tắc: **state nâng lên store chỉ khi thực sự cần chia sẻ.** Giống không phải class nào cũng cần là `@Service` singleton.

---

## 7. 🧠 Tự kiểm tra

1. Vì sao danh mục nên ở store mà filter của bảng giao dịch thì không?
2. `storeToRefs` để làm gì? Điều gì xảy ra nếu destructure thẳng `const { items } = store`?
3. State / getters / actions của Pinia ánh xạ sang khái niệm component nào?
4. `defineStore('categories', ...)` — chuỗi `'categories'` đóng vai trò gì? Gọi `useCategoriesStore()` ở 2 component có ra 2 instance khác nhau không?
5. Vì sao sau khi `store.create()` không cần gọi `refresh()` ở component nữa?

---

## 8. Kết quả mong đợi

- [ ] `stores/categories.ts` hoạt động, Pinia đã cài.
- [ ] Categories + Transactions cùng đọc store; thêm ở 1 nơi → nơi kia thấy ngay.
- [ ] Hiểu storeToRefs và khi nào nên/không nên đưa state lên store.

→ Tiếp: [`07-reports-dashboard.md`](07-reports-dashboard.md) — dựng Dashboard với thẻ số liệu + biểu đồ.
