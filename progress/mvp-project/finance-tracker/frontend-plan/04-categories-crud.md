# 04 — Categories CRUD (reactivity + form + modal)

> **Mục tiêu phase này:** CRUD category đầy đủ: thêm (modal có form), sửa, xóa. Đây là phase **quan trọng nhất về tư duy Vue** — hiểu reactivity, `v-model`, sự kiện. Nắm chắc phase này thì Transactions (Phase 05) chỉ là lặp lại ở quy mô lớn hơn.

---

## 1. Reactivity — khái niệm cốt lõi, đọc chậm

Đây là chỗ dân Java hay khựng. Trong Java/Spring MVC: bạn render HTML 1 lần, xong. Muốn đổi giao diện → request mới.

Trong Vue: bạn khai báo **biến reactive**. Khi giá trị biến đổi → **UI tự render lại phần liên quan**, không cần bạn động tay vào DOM. Giống Flutter `setState`/reactive state, hoặc binding 2 chiều của Angular.

```ts
const count = ref(0)          // biến reactive, giá trị nằm ở count.value
count.value++                 // đổi value -> mọi {{ count }} trên template tự cập nhật
```

Hai cách tạo state reactive:
- **`ref(x)`** — cho giá trị đơn (số, chuỗi, boolean, hoặc cả object). Trong `<script>` truy cập qua `.value`; trong `<template>` Vue tự bỏ `.value` cho bạn.
- **`reactive({...})`** — cho object/form. Truy cập trực tiếp `obj.field` (không `.value`).

> ⚠️ Bẫy kinh điển: trong `<script setup>` quên `.value`.
> ```ts
> const name = ref('a')
> name = 'b'        // ❌ SAI — ghi đè cả ref
> name.value = 'b'  // ✅ ĐÚNG
> ```
> Trong `<template>` thì viết `{{ name }}` (không `.value`) — Vue tự lo.

### `computed` — giá trị dẫn xuất
```ts
const incomeCount = computed(() =>
  categories.value?.filter(c => c.type === 'income').length ?? 0
)
```
`computed` tự tính lại **chỉ khi** dependency (`categories`) đổi, và cache kết quả. Giống một getter dẫn xuất / `@Formula` của Hibernate. Đừng nhét logic nặng vào template — đẩy vào `computed`.

---

## 2. `v-model` — binding 2 chiều cho form

```vue
<UInput v-model="form.name" />
```
`v-model` = gắn input với biến: gõ vào input → biến đổi; đổi biến bằng code → input đổi. **Hai chiều.** Tương đương `[(ngModel)]` của Angular, hay binding form của Flutter.

Bên Spring bạn submit cả form rồi bind vào DTO ở server. Ở đây binding xảy ra **realtime ngay trên client**, từng ký tự.

---

## 3. ✅ Bổ sung state + modal vào trang Categories

Ta dùng component Nuxt UI: `UModal`, `UForm`, `UButton`, `USelect`, `UInput`, `UTable`.

`pages/categories.vue` (mở rộng từ Phase 03):

```vue
<script setup lang="ts">
import type { Category } from '~/types'

const api = useApi()
const { data: categories, refresh } = await useFetch(() => api.categories.list(), { key: 'categories' })

// --- state cho modal + form ---
const open = ref(false)                 // modal mở hay đóng
const editingId = ref<number | null>(null)  // null = đang TẠO MỚI, có id = đang SỬA

// form reactive. Dùng reactive cho object nhiều field.
const form = reactive({
  name: '',
  type: 'expense' as 'income' | 'expense',
  icon: '',
  color: '#3b82f6',
})

const typeOptions = [
  { label: 'Chi (expense)', value: 'expense' },
  { label: 'Thu (income)', value: 'income' },
]

// Mở modal ở chế độ TẠO MỚI: reset form
function openCreate() {
  editingId.value = null
  Object.assign(form, { name: '', type: 'expense', icon: '', color: '#3b82f6' })
  open.value = true
}

// Mở modal ở chế độ SỬA: đổ dữ liệu category vào form
function openEdit(cat: Category) {
  editingId.value = cat.id
  Object.assign(form, { name: cat.name, type: cat.type, icon: cat.icon ?? '', color: cat.color ?? '#3b82f6' })
  open.value = true
}

// Submit: tạo mới hoặc cập nhật tùy editingId
async function save() {
  if (editingId.value === null) {
    await api.categories.create({ ...form })
  } else {
    await api.categories.update(editingId.value, { ...form })
  }
  open.value = false
  await refresh()   // tải lại danh sách để thấy thay đổi
}

async function remove(id: number) {
  if (!confirm('Xóa danh mục này?')) return
  await api.categories.remove(id)
  await refresh()
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h1 class="text-xl font-bold">Danh mục</h1>
      <UButton icon="i-lucide-plus" @click="openCreate">Thêm danh mục</UButton>
    </div>

    <!-- Danh sách -->
    <div class="space-y-2">
      <div
        v-for="cat in categories"
        :key="cat.id"
        class="flex items-center gap-3 border rounded p-3"
      >
        <span :style="{ color: cat.color ?? '#888' }" class="text-lg">{{ cat.icon || '•' }}</span>
        <span class="flex-1">{{ cat.name }}</span>
        <UBadge :color="cat.type === 'income' ? 'success' : 'error'">{{ cat.type }}</UBadge>
        <UButton size="xs" variant="ghost" icon="i-lucide-pencil" @click="openEdit(cat)" />
        <UButton size="xs" variant="ghost" color="error" icon="i-lucide-trash" @click="remove(cat.id)" />
      </div>
    </div>

    <!-- Modal thêm/sửa -->
    <UModal v-model:open="open" :title="editingId === null ? 'Thêm danh mục' : 'Sửa danh mục'">
      <template #body>
        <div class="space-y-4">
          <UFormField label="Tên">
            <UInput v-model="form.name" placeholder="VD: Ăn uống" class="w-full" />
          </UFormField>
          <UFormField label="Loại">
            <USelect v-model="form.type" :items="typeOptions" class="w-full" />
          </UFormField>
          <UFormField label="Icon (emoji hoặc text)">
            <UInput v-model="form.icon" placeholder="🍜" class="w-full" />
          </UFormField>
          <UFormField label="Màu">
            <input v-model="form.color" type="color" class="h-9 w-16" />
          </UFormField>
        </div>
      </template>
      <template #footer>
        <UButton variant="ghost" @click="open = false">Hủy</UButton>
        <UButton @click="save">Lưu</UButton>
      </template>
    </UModal>
  </div>
</template>
```

---

## 4. Mổ xẻ những điểm mới

- **`@click="openCreate"`** = lắng nghe sự kiện click. `@` là viết tắt của `v-on:`. Giống `onclick` nhưng gọi method Vue. (Spring không có khái niệm tương đương phía client — đây là event handler thuần client.)
- **`v-model:open="open"`** — `UModal` expose 1 prop `open` 2 chiều. Khi user bấm ra ngoài để đóng, biến `open` của bạn tự thành `false`. Đây là `v-model` có **đối số** (`:open`).
- **`<template #body>` / `#footer`** = điền vào **named slot** của `UModal`. Component cha (UModal) chừa sẵn các "lỗ" tên `body`, `footer`; bạn nhét nội dung vào. (`#body` là viết tắt `v-slot:body`.)
- **`{ ...form }`** = **spread**, copy nông các field của `form` thành object mới. Tránh gửi thẳng object reactive đi. (Như tạo bản sao DTO.)
- **`editingId` quyết định create vs update** — 1 modal dùng cho cả 2 việc. Pattern rất phổ biến, nhớ lấy.
- **`confirm(...)`** = hộp thoại xác nhận của trình duyệt. Tạm dùng; Phase 08 thay bằng modal đẹp hơn.

> 💡 Vì sao `form` dùng `reactive` còn `open`/`editingId` dùng `ref`? — `reactive` hợp cho **object nhiều field** (form), `ref` hợp cho **giá trị đơn**. Cả 2 đều reactive; chọn theo hình dạng dữ liệu.

---

## 5. Luồng dữ liệu CRUD (vẽ trong đầu)

```
User bấm "Thêm"  → openCreate(): reset form, open=true → modal hiện
User gõ form     → v-model cập nhật form realtime
User bấm "Lưu"   → save(): $fetch POST → backend tạo → refresh() tải lại list → UI update
```
Khác Spring MVC (submit → server render lại cả trang): ở đây chỉ vùng danh sách re-render, không reload. Đó là sức mạnh của reactivity + SPA.

---

## 6. 🧠 Tự kiểm tra

1. Vì sao trong `<script>` phải viết `open.value` nhưng trong `<template>` chỉ cần `open`?
2. `ref` và `reactive` khác nhau khi nào dùng cái nào?
3. Một modal làm sao phục vụ cả "thêm" lẫn "sửa"? Biến nào quyết định?
4. `@click` và `v-model` — cái nào là 1 chiều, cái nào 2 chiều?
5. Sau khi POST tạo category, vì sao phải gọi `refresh()`? Nếu bỏ thì sao?
6. `{ ...form }` làm gì? Vì sao không gửi thẳng `form`?

---

## 7. Kết quả mong đợi

- [ ] Thêm category mới qua modal → xuất hiện trong list.
- [ ] Sửa category → cập nhật đúng.
- [ ] Xóa category → biến mất.
- [ ] Hiểu reactivity (`ref`/`reactive`/`computed`), `v-model`, `@click`, slot.

→ Tiếp: [`05-transactions-crud.md`](05-transactions-crud.md) — màn phức tạp hơn: filter, phân trang, tách component con.
