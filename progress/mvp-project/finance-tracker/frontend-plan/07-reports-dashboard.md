# 07 — Reports & Dashboard (thẻ số liệu + biểu đồ)

> **Mục tiêu phase này:** Dựng trang Dashboard: 3 thẻ tổng quan (thu/chi/số dư), biểu đồ thu-chi theo tháng, biểu đồ chi theo danh mục. Học gọi **nhiều API song song** và tích hợp **thư viện biểu đồ**.
> Cuối phase: vào `/` thấy dashboard sống động — đây là màn "khoe được".

---

## 1. Mở rộng lớp API cho reports

Thêm types vào `types/index.ts`:
```ts
export interface MonthlyItem {
  year: number
  month: number
  total_income: string
  total_expense: string
  balance: string
}
export interface ByCategoryItem {
  category_id: number
  category_name: string
  type: string
  total: string
}
```

Thêm vào `useApi()`:
```ts
reports: {
  summary: () => $fetch<Summary>(`${base}/reports/summary`),
  monthly: () => $fetch<{ items: MonthlyItem[] }>(`${base}/reports/monthly`),
  byCategory: () => $fetch<{ items: ByCategoryItem[] }>(`${base}/reports/by-category`),
},
```

---

## 2. Gọi nhiều API song song

Dashboard cần 3 nguồn dữ liệu. Gọi tuần tự thì chậm (chờ cái này xong mới gọi cái kia). Gọi **song song** bằng `Promise.all` — giống `CompletableFuture.allOf` bên Java.

`pages/index.vue`:
```vue
<script setup lang="ts">
const api = useApi()

const { data } = await useAsyncData('dashboard', async () => {
  const [summary, monthly, byCategory] = await Promise.all([
    api.reports.summary(),
    api.reports.monthly(),
    api.reports.byCategory(),
  ])
  return { summary, monthly: monthly.items, byCategory: byCategory.items }
})

function money(v: string | number) {
  return Number(v).toLocaleString('vi-VN') + ' đ'
}
</script>
```

> **`useAsyncData`** = anh em của `useFetch`, dùng khi cần **logic tải tùy biến** (ở đây: gộp 3 call). `useFetch(url)` chỉ là `useAsyncData` + `$fetch` đóng gói sẵn. Đối số đầu `'dashboard'` là **key cache** (như Phase 03).
> `Promise.all([...])` chạy 3 request cùng lúc, chờ cả 3 xong. Nhanh hơn `await` từng cái.

---

## 3. ✅ Thẻ số liệu (summary cards)

```vue
<template>
  <div>
    <h1 class="text-xl font-bold mb-6">Dashboard</h1>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      <UCard>
        <div class="text-sm text-gray-500">Tổng thu</div>
        <div class="text-2xl font-bold text-green-600">{{ money(data!.summary.total_income) }}</div>
      </UCard>
      <UCard>
        <div class="text-sm text-gray-500">Tổng chi</div>
        <div class="text-2xl font-bold text-red-600">{{ money(data!.summary.total_expense) }}</div>
      </UCard>
      <UCard>
        <div class="text-sm text-gray-500">Số dư</div>
        <div class="text-2xl font-bold">{{ money(data!.summary.balance) }}</div>
      </UCard>
    </div>

    <!-- biểu đồ ở mục 4 -->
  </div>
</template>
```
- **`grid grid-cols-1 md:grid-cols-3`** = Tailwind responsive: mobile 1 cột, màn vừa trở lên (`md:`) 3 cột. Tự co giãn theo màn hình.
- **`data!`** — dấu `!` là "non-null assertion" của TS: ta khẳng định `data` không null ở điểm này (vì đã `await`). Java không có cú pháp này, nhưng ý tương tự ép kiểu chắc-chắn-không-null.

---

## 4. Biểu đồ — cài & dùng Chart.js

Cách phổ biến & dễ học: **Chart.js** qua wrapper **vue-chartjs**.

```bash
npm install chart.js vue-chartjs
```

> ⚠️ Chart.js đụng tới DOM/`window` nên **chỉ chạy phía client**. Trong Nuxt (mặc định SSR), phải đảm bảo component chart **không render lúc server-side**. Cách đơn giản nhất: đặt file chart vào `components/` với hậu tố `.client.vue` → Nuxt **chỉ render phía client**. (Đây là một nét đặc thù SSR của Nuxt — server không có `window`.)

Tạo `components/MonthlyChart.client.vue`:
```vue
<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale,
} from 'chart.js'
import type { MonthlyItem } from '~/types'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps<{ items: MonthlyItem[] }>()

// computed: biến data backend -> format Chart.js cần
const chartData = computed(() => ({
  labels: props.items.map(m => `${m.month}/${m.year}`),
  datasets: [
    { label: 'Thu', data: props.items.map(m => Number(m.total_income)), backgroundColor: '#16a34a' },
    { label: 'Chi', data: props.items.map(m => Number(m.total_expense)), backgroundColor: '#dc2626' },
  ],
}))
</script>

<template>
  <Bar :data="chartData" :options="{ responsive: true }" />
</template>
```

Dùng trong dashboard:
```vue
<UCard class="mb-6">
  <template #header><b>Thu chi theo tháng</b></template>
  <MonthlyChart :items="data!.monthly" />
</UCard>
```

> 🧠 Để ý: ta lại dùng **props** (truyền `items` xuống chart) và **computed** (biến đổi data sang format Chart.js). Toàn khái niệm đã học — chỉ ghép lại. Đó là dấu hiệu bạn đang tiến bộ: thứ mới (Chart.js) gắn vào khung cũ (props/computed) đã quen.

Biểu đồ "chi theo danh mục" làm tương tự với `Pie`/`Doughnut` từ `vue-chartjs`, lọc `byCategory` lấy `type === 'expense'`. Tự làm như bài tập.

---

## 5. 🧠 Tự kiểm tra

1. Vì sao dùng `Promise.all` thay vì `await` 3 API lần lượt? Lợi gì?
2. `useAsyncData` khác `useFetch` chỗ nào? Khi nào chọn cái nào?
3. Vì sao file chart phải là `.client.vue`? Điều gì xảy ra nếu render Chart.js phía server?
4. `data!` — dấu `!` nghĩa là gì? Có rủi ro không?
5. Component chart nhận dữ liệu qua cơ chế nào? Biến đổi format bằng cái gì?

---

## 6. Kết quả mong đợi

- [ ] Dashboard có 3 thẻ thu/chi/số dư đúng số liệu.
- [ ] Biểu đồ cột thu-chi theo tháng hiển thị.
- [ ] (Bài tập) biểu đồ tròn chi theo danh mục.
- [ ] Hiểu `Promise.all`, `useAsyncData`, và vì sao chart phải client-only.

→ Tiếp: [`08-hoan-thien-deploy.md`](08-hoan-thien-deploy.md) — đánh bóng UX, xử lý lỗi, build & deploy.
