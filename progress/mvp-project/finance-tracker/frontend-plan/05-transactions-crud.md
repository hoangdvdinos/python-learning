# 05 — Transactions CRUD (filter + phân trang + component con)

> **Mục tiêu phase này:** Màn Giao dịch — bảng dữ liệu, filter (loại/danh mục/khoảng ngày), phân trang, và CRUD. Học cách **state đổi → tự gọi lại API** (`watch`), và **tách component con** truyền dữ liệu qua **props/emit**.
> Đây là phase tổng hợp mọi thứ đã học + thêm 2 khái niệm mới (watch, props/emit).

---

## 1. Mở rộng lớp API cho transactions

Thêm vào `composables/useApi.ts` (trong object trả về của `useApi`):

```ts
import type { Transaction } from '~/types'

// kiểu tham số filter — khớp query params của backend
export interface TxFilter {
  type?: 'income' | 'expense'
  category_id?: number
  date_from?: string
  date_to?: string
  page?: number
  size?: number
}

// ... trong return { ... } thêm:
transactions: {
  list: (filter: TxFilter = {}) =>
    $fetch<Transaction[]>(`${base}/transactions`, { query: filter }),
  create: (body: Record<string, unknown>) =>
    $fetch<Transaction>(`${base}/transactions`, { method: 'POST', body }),
  update: (id: number, body: Record<string, unknown>) =>
    $fetch<Transaction>(`${base}/transactions/${id}`, { method: 'PATCH', body }),
  remove: (id: number) =>
    $fetch(`${base}/transactions/${id}`, { method: 'DELETE' }),
},
```

> Backend nhận filter qua query string (`?type=expense&page=2&size=20`). Nuxt `{ query: filter }` tự bỏ field `undefined`, nên không cần xử lý tay.

---

## 2. `watch` — "state đổi thì làm gì đó"

Khái niệm mới: ta muốn **mỗi khi filter hoặc trang đổi → tự gọi lại API**. Đó là việc của `watch` (hoặc `useFetch` với key động).

```ts
const filter = reactive<TxFilter>({ page: 1, size: 20 })

// useFetch nhận hàm => khi giá trị bên trong đổi, ta gọi refresh.
// Cách gọn nhất: dùng watch để refresh khi filter đổi.
const { data: txs, refresh } = await useFetch(() => api.transactions.list(filter), {
  key: 'transactions',
  watch: [filter],   // 👈 filter đổi -> useFetch tự gọi lại. Không cần watch thủ công!
})
```

> 💡 `useFetch` có option `watch` — liệt kê các nguồn reactive cần "theo dõi"; chúng đổi thì tự fetch lại. Đây là cách Nuxt-ish nhất. (Nếu cần logic phức tạp hơn mới viết `watch(() => ..., () => {...})` riêng — tương tự `@PostUpdate` listener, nhưng cho state client.)

Đổi `filter.type = 'expense'` ở đâu đó → bảng tự load lại. Đổi `filter.page = 2` → trang sau tự về. **Đây là điểm "wow" của reactivity**: bạn mô tả *quan hệ* (filter ↔ data), không viết lệnh *gọi lại* mỗi chỗ.

---

## 3. ✅ Trang Transactions

`pages/transactions.vue`:

```vue
<script setup lang="ts">
import type { TxFilter } from '~/composables/useApi'

const api = useApi()

// danh mục để đổ vào ô filter + form (lấy 1 lần)
const { data: categories } = await useFetch(() => api.categories.list(), { key: 'categories' })

const filter = reactive<TxFilter>({ page: 1, size: 20 })
const { data: txs, refresh } = await useFetch(() => api.transactions.list(filter), {
  key: 'transactions',
  watch: [filter],
})

const typeItems = [
  { label: 'Tất cả', value: undefined },
  { label: 'Thu', value: 'income' },
  { label: 'Chi', value: 'expense' },
]

function money(v: string) {
  return Number(v).toLocaleString('vi-VN') + ' đ'
}

async function remove(id: number) {
  if (!confirm('Xóa giao dịch?')) return
  await api.transactions.remove(id)
  await refresh()
}
</script>

<template>
  <div>
    <h1 class="text-xl font-bold mb-4">Giao dịch</h1>

    <!-- Bộ lọc -->
    <div class="flex gap-3 mb-4 items-end flex-wrap">
      <USelect v-model="filter.type" :items="typeItems" placeholder="Loại" class="w-40" />
      <UInput v-model="filter.date_from" type="date" />
      <UInput v-model="filter.date_to" type="date" />
    </div>

    <!-- Bảng -->
    <div class="border rounded divide-y">
      <div
        v-for="t in txs"
        :key="t.id"
        class="flex items-center gap-3 p-3"
      >
        <span class="w-28 text-sm text-gray-500">{{ t.transaction_date }}</span>
        <span class="flex-1">{{ t.description || t.category.name }}</span>
        <UBadge variant="subtle">{{ t.category.name }}</UBadge>
        <span :class="t.type === 'income' ? 'text-green-600' : 'text-red-600'" class="w-32 text-right font-medium">
          {{ t.type === 'income' ? '+' : '-' }}{{ money(t.amount) }}
        </span>
        <UButton size="xs" variant="ghost" color="error" icon="i-lucide-trash" @click="remove(t.id)" />
      </div>
      <p v-if="!txs?.length" class="p-4 text-gray-400 text-center">Chưa có giao dịch.</p>
    </div>

    <!-- Phân trang đơn giản -->
    <div class="flex gap-2 mt-4 items-center">
      <UButton :disabled="filter.page === 1" @click="filter.page!--">Trước</UButton>
      <span>Trang {{ filter.page }}</span>
      <UButton :disabled="(txs?.length ?? 0) < filter.size!" @click="filter.page!++">Sau</UButton>
    </div>
  </div>
</template>
```

Quan sát:
- Đổi ô filter / bấm "Trước-Sau" → `filter` đổi → bảng **tự** load lại nhờ `watch: [filter]`. Không có dòng nào gọi `refresh()` ở đây cả!
- **`:class="..."`** = bind class động: thu → xanh, chi → đỏ.
- `money()` = hàm format tiền dùng `Intl` của trình duyệt. `Number(t.amount)` vì `amount` là string (nhớ Phase 03).
- Phân trang ở đây "ngây thơ" (nút Sau tắt khi trang trả về ít hơn `size`). Backend chưa trả tổng số trang nên tạm vậy — đủ học.

> Form **thêm giao dịch**: làm tương tự modal ở Phase 04, nhưng có thêm `USelect` chọn category (lấy từ `categories`), `UInput type="number"` cho amount, `type="date"` cho ngày. Tự làm như bài tập — bạn đã có đủ công cụ.

---

## 4. Tách component con + props/emit (khái niệm mới quan trọng)

Khi 1 trang phình to, ta **tách phần con ra component riêng** để dễ đọc & tái dùng. Ví dụ tách 1 dòng giao dịch thành `components/TransactionRow.vue`.

Cách 2 component "nói chuyện":
- **props** = cha truyền dữ liệu **xuống** con (1 chiều, read-only). Giống tham số constructor / `@Input` của Angular.
- **emit** = con bắn sự kiện **lên** cha. Giống `@Output`/callback. (Con KHÔNG sửa thẳng dữ liệu của cha — nó báo "này, user bấm xóa" rồi cha tự xử.)

`components/TransactionRow.vue`:
```vue
<script setup lang="ts">
import type { Transaction } from '~/types'

// nhận 1 transaction từ cha
const props = defineProps<{ tx: Transaction }>()

// khai báo các sự kiện sẽ bắn lên cha
const emit = defineEmits<{ delete: [id: number] }>()

function money(v: string) {
  return Number(v).toLocaleString('vi-VN') + ' đ'
}
</script>

<template>
  <div class="flex items-center gap-3 p-3">
    <span class="w-28 text-sm text-gray-500">{{ tx.transaction_date }}</span>
    <span class="flex-1">{{ tx.description || tx.category.name }}</span>
    <UBadge variant="subtle">{{ tx.category.name }}</UBadge>
    <span :class="tx.type === 'income' ? 'text-green-600' : 'text-red-600'" class="w-32 text-right font-medium">
      {{ tx.type === 'income' ? '+' : '-' }}{{ money(tx.amount) }}
    </span>
    <UButton size="xs" variant="ghost" color="error" icon="i-lucide-trash" @click="emit('delete', tx.id)" />
  </div>
</template>
```

Dùng trong trang (thay vòng `v-for` cũ):
```vue
<TransactionRow
  v-for="t in txs"
  :key="t.id"
  :tx="t"
  @delete="remove"
/>
```
- `:tx="t"` = truyền prop xuống con.
- `@delete="remove"` = lắng nghe sự kiện `delete` con bắn lên, gọi `remove`.
- `TransactionRow` **auto-import** vì nằm trong `components/`.

> 📌 Quy tắc vàng: **dữ liệu chảy xuống (props), sự kiện bay lên (emit)**. "Props down, events up." Con không bao giờ tự ý sửa data của cha — nó xin phép qua emit. Giúp luồng dữ liệu 1 chiều, dễ debug. (Khác với để con sửa lung tung state cha — sẽ rối như canh hẹ.)

---

## 5. 🧠 Tự kiểm tra

1. Vì sao đổi `filter.type` thì bảng tự load lại mà mình không gọi `refresh()`? Cơ chế nào?
2. `watch: [filter]` trong `useFetch` làm gì?
3. props và emit khác nhau ra sao? Cái nào đi xuống, cái nào đi lên?
4. Vì sao component con không nên tự sửa prop nhận từ cha?
5. `Number(t.amount)` — vì sao phải `Number(...)`? `amount` đang là kiểu gì?
6. `TransactionRow` đặt ở `components/` thì có cần `import` khi dùng không? Vì sao?

---

## 6. Kết quả mong đợi

- [ ] Bảng giao dịch hiển thị data thật, format tiền + màu thu/chi.
- [ ] Filter loại/ngày đổi → bảng tự cập nhật.
- [ ] Phân trang Trước/Sau hoạt động.
- [ ] Xóa giao dịch hoạt động; (thêm/sửa làm như bài tập).
- [ ] Đã tách `TransactionRow.vue`, hiểu props/emit.

→ Tiếp: [`06-state-pinia.md`](06-state-pinia.md) — chia sẻ state (danh mục) toàn app, hết phải fetch lặp.
