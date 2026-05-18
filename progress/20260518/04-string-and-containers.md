# 04 — String & Container

> **Khối 3 — String & Container**
> Dành cho Java developer — tập trung vào điểm khác biệt so với Java.

---

## 1. String — Chuỗi Ký Tự

### 1.1 Tính Bất Biến (Immutable) & Indexing

> **Java developer chú ý:** String Python cũng immutable giống Java `String`. Mọi thao tác "sửa" đều tạo ra object mới — không thay đổi tại chỗ.

```python
text = "Hello, Python"

# Indexing — truy cập từng ký tự (Java: text.charAt(0))
print(text[0])      # H
print(text[-1])     # n  ← Chỉ số âm: đếm từ cuối — Java KHÔNG có
print(text[-3])     # h

# Slicing — cắt chuỗi con (Java: text.substring(start, end))
# Cú pháp: text[start:stop:step]
print(text[0:5])    # Hello  — Java: text.substring(0, 5)
print(text[7:])     # Python — từ index 7 đến hết
print(text[:5])     # Hello  — từ đầu đến index 5 (không gồm 5)
print(text[::2])    # Hlo yhn — bước nhảy 2
print(text[::-1])   # nohtyP ,olleH — đảo ngược chuỗi

# Immutable — không thể sửa trực tiếp
# text[0] = "h"   # TypeError: 'str' object does not support item assignment
```

| Đặc điểm         | Java                    | Python                    |
|------------------|-------------------------|---------------------------|
| Truy cập ký tự   | `text.charAt(i)`        | `text[i]`                 |
| Chỉ số âm        | Không có                | `text[-1]` = ký tự cuối   |
| Cắt chuỗi con    | `text.substring(a, b)`  | `text[a:b]`               |
| Đảo ngược        | `new StringBuilder(text).reverse().toString()` | `text[::-1]` |
| Immutable        | Có                      | Có                        |

### 1.2 Các Phương Thức Xử Lý String Thường Dùng

```python
s = "  Hello, Python World!  "

# Thay đổi chữ hoa/thường
print(s.upper())          # "  HELLO, PYTHON WORLD!  "
print(s.lower())          # "  hello, python world!  "
print(s.title())          # "  Hello, Python World!  "  — viết hoa đầu mỗi từ
print(s.capitalize())     # "  hello, python world!  " với chữ đầu tiên viết hoa

# Xóa khoảng trắng (Java: text.trim())
print(s.strip())          # "Hello, Python World!"  — xóa cả hai đầu
print(s.lstrip())         # "Hello, Python World!  " — xóa trái
print(s.rstrip())         # "  Hello, Python World!" — xóa phải

# Thay thế (Java: text.replace("a", "b"))
sentence = "I love Java, Java is great"
print(sentence.replace("Java", "Python"))       # "I love Python, Python is great"
print(sentence.replace("Java", "Python", 1))   # Chỉ thay lần đầu tiên

# Tìm kiếm
text = "Hello, Python"
print(text.find("Python"))     # 7  — Java: text.indexOf("Python")
print(text.find("Java"))       # -1 — Không tìm thấy trả về -1
print(text.index("Python"))    # 7  — Tương tự find nhưng ném ValueError nếu không tìm thấy
print("Python" in text)        # True — kiểm tra nhanh hơn (không cần indexOf)

# Kiểm tra bắt đầu / kết thúc
print(text.startswith("Hello"))   # True  — Java: text.startsWith("Hello")
print(text.endswith("Python"))    # True  — Java: text.endsWith("Python")

# Đếm số lần xuất hiện
print("banana".count("an"))       # 2
```

### 1.3 `split` và `join`

```python
# split — tách chuỗi thành List (Java: text.split(","))
csv = "alice,bob,charlie,dave"
names = csv.split(",")
print(names)            # ['alice', 'bob', 'charlie', 'dave']

# Giới hạn số lần tách
parts = csv.split(",", 2)
print(parts)            # ['alice', 'bob', 'charlie,dave']

# Tách theo khoảng trắng (mặc định — nhiều khoảng trắng cũng OK)
sentence = "  Hello   Python   World  "
words = sentence.split()
print(words)            # ['Hello', 'Python', 'World']

# join — nối List thành chuỗi
# Cú pháp: separator.join(list) — Java: String.join(",", list)
names = ["alice", "bob", "charlie"]
print(", ".join(names))     # "alice, bob, charlie"
print(" - ".join(names))    # "alice - bob - charlie"
print("".join(names))       # "alicebobcharlie"

# Pattern phổ biến: split → xử lý → join
tags = "  python,  fastapi,  backend  "
clean_tags = ", ".join(tag.strip() for tag in tags.split(","))
print(clean_tags)       # "python, fastapi, backend"
```

> **Java developer chú ý:** `join` trong Python là method của **separator string**, không phải method của list.
> - Java: `String.join(",", list)`
> - Python: `",".join(list)`

### 1.4 Định Dạng Chuỗi (String Formatting)

Python có 3 cách format — chỉ cần nhớ **f-string** (hiện đại nhất).

```python
name = "Hoàng"
age = 28
salary = 25_000_000.5

# Cách 1: f-string (Python 3.6+) — KHUYẾN NGHỊ dùng
# Tương tự String.format() của Java nhưng ngắn hơn nhiều
print(f"Xin chào {name}, {age} tuổi")          # Xin chào Hoàng, 28 tuổi
print(f"Lương: {salary:,.0f} VND")              # Lương: 25,000,001 VND
print(f"Tỉ lệ: {0.1256:.2%}")                  # Tỉ lệ: 12.56%
print(f"Hex: {255:#010x}")                      # Hex: 0x000000ff
print(f"Căn chỉnh: |{name:^20}|")              # |       Hoàng        |
print(f"Số: {age:05d}")                         # Số: 00028

# Debug expression (Python 3.8+) — rất tiện khi debug
x = 42
print(f"{x = }")        # x = 42 — in cả tên biến lẫn giá trị
```

```python
# Cách 2: .format() — Python 3.0+, ít dùng hơn f-string
# Tương tự nhất với String.format() Java
print("Xin chào {}, {} tuổi".format(name, age))
print("Xin chào {name}, {age} tuổi".format(name=name, age=age))
print("Lương: {:,.0f} VND".format(salary))

# Cách 3: % operator — cũ, tránh dùng trong code mới
print("Xin chào %s, %d tuổi" % (name, age))
```

| Cú pháp format | Ưu điểm                        | Khi nào dùng                  |
|----------------|--------------------------------|-------------------------------|
| f-string       | Ngắn gọn, rõ ràng, nhanh nhất | Mặc định — luôn dùng          |
| `.format()`    | Linh hoạt hơn với template     | Khi template tách biệt với data |
| `%` operator   | —                              | Tránh dùng — cú pháp cũ       |

---

## 2. List — Danh Sách Có Thứ Tự

### 2.1 Khởi Tạo, Truy Cập, Slicing

> **Java developer:** List trong Python giống `ArrayList<Object>` nhưng có thể chứa nhiều kiểu cùng lúc và hỗ trợ slicing.

```python
# Khởi tạo
fruits = ["apple", "banana", "cherry"]
mixed = [1, "hello", True, 3.14, None]  # Khác Java — nhiều kiểu cùng lúc
empty = []
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # List lồng nhau

# Truy cập — tương tự Java: list.get(i)
print(fruits[0])        # apple
print(fruits[-1])       # cherry — chỉ số âm
print(fruits[-2])       # banana

# Slicing — Java: list.subList(a, b)
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(numbers[2:5])     # [2, 3, 4]
print(numbers[:3])      # [0, 1, 2]
print(numbers[7:])      # [7, 8, 9]
print(numbers[::2])     # [0, 2, 4, 6, 8]
print(numbers[::-1])    # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0] — đảo ngược

# Kiểm tra độ dài
print(len(fruits))      # 3 — Java: fruits.size()
```

### 2.2 Các Phương Thức Xử Lý List

```python
fruits = ["apple", "banana"]

# Thêm phần tử
fruits.append("cherry")        # Thêm cuối — Java: list.add(item)
fruits.insert(1, "avocado")    # Thêm vào vị trí 1 — Java: list.add(1, item)
print(fruits)   # ['apple', 'avocado', 'banana', 'cherry']

# extend — nối thêm một list khác (Java: list.addAll(other))
fruits.extend(["date", "elderberry"])
print(fruits)   # ['apple', 'avocado', 'banana', 'cherry', 'date', 'elderberry']

# Khác biệt append vs extend
a = [1, 2, 3]
a.append([4, 5])    # [[4, 5]] là 1 phần tử
print(a)            # [1, 2, 3, [4, 5]]

b = [1, 2, 3]
b.extend([4, 5])    # 4 và 5 là 2 phần tử riêng
print(b)            # [1, 2, 3, 4, 5]
```

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

# Xóa phần tử
numbers.remove(1)       # Xóa lần xuất hiện đầu tiên của giá trị 1 — Java: list.remove(Integer.valueOf(1))
popped = numbers.pop()  # Xóa và trả về phần tử cuối — Java: list.remove(list.size()-1)
popped2 = numbers.pop(0)# Xóa và trả về phần tử tại index 0
print(numbers)          # [4, 1, 5, 9, 6]

# Sắp xếp
nums = [3, 1, 4, 1, 5, 9, 2, 6]
nums.sort()                     # Sắp xếp tại chỗ (in-place) — Java: Collections.sort(list)
print(nums)                     # [1, 1, 2, 3, 4, 5, 6, 9]
nums.sort(reverse=True)         # Giảm dần
print(nums)                     # [9, 6, 5, 4, 3, 2, 1, 1]

# sorted() — trả về list mới, không sửa list gốc
original = [3, 1, 4, 1, 5]
new_sorted = sorted(original)   # Java: new ArrayList(list); Collections.sort(new_list)
print(original)                 # [3, 1, 4, 1, 5] — không thay đổi
print(new_sorted)               # [1, 1, 3, 4, 5]

# Các phương thức khác
data = [1, 2, 3, 2, 1]
print(data.count(2))    # 2 — đếm số lần xuất hiện
print(data.index(3))    # 2 — vị trí đầu tiên — Java: list.indexOf(3)
data.reverse()          # Đảo ngược tại chỗ
data.clear()            # Xóa toàn bộ — Java: list.clear()
```

### 2.3 Queue và Stack Dùng List

```python
# Stack (LIFO) — dùng append/pop
stack = []
stack.append(1)     # push — Java: stack.push(1)
stack.append(2)
stack.append(3)
print(stack.pop())  # 3 — pop từ cuối — Java: stack.pop()
print(stack.pop())  # 2

# Queue (FIFO) — dùng collections.deque (hiệu quả hơn list)
from collections import deque

queue = deque()
queue.append("A")       # enqueue — Java: queue.offer("A")
queue.append("B")
queue.append("C")
print(queue.popleft())  # A — dequeue từ đầu — Java: queue.poll()
print(queue.popleft())  # B

# Nếu dùng list làm Queue — kém hiệu quả vì pop(0) phải dịch chuyển toàn bộ
# Nên dùng deque cho Queue
```

> **Tại sao `deque` cho Queue?** `list.pop(0)` là O(n) — phải dịch chuyển toàn bộ phần tử. `deque.popleft()` là O(1).

### 2.4 List Comprehension và Tối Ưu Mã Nguồn

```python
# Đã học ở Khối 2 — ôn lại nhanh và thêm pattern nâng cao
numbers = list(range(1, 11))

# Pattern cơ bản: [biểu_thức for item in iterable if điều_kiện]
squares = [n ** 2 for n in numbers]
evens = [n for n in numbers if n % 2 == 0]

# Nested comprehension — tạo ma trận
matrix = [[i * j for j in range(1, 4)] for i in range(1, 4)]
print(matrix)
# [[1, 2, 3], [2, 4, 6], [3, 6, 9]]

# Flatten matrix
flat = [val for row in matrix for val in row]
print(flat)     # [1, 2, 3, 2, 4, 6, 3, 6, 9]

# Comprehension vs map/filter — comprehension thường dễ đọc hơn
names = ["alice", "bob", "charlie"]

# Cách cũ — Java stream style
upper_map = list(map(str.upper, names))

# Python style — comprehension dễ đọc hơn
upper_comp = [name.upper() for name in names]
```

---

## 3. Tuple — Danh Sách Bất Biến

### 3.1 Tìm Hiểu Tuple

> **Java developer:** Tuple giống `List` nhưng **immutable** sau khi tạo. Java không có kiểu dữ liệu tương đương trực tiếp (gần nhất là `List.of()` — unmodifiable list).

```python
# Khởi tạo Tuple
point = (3, 7)
colors = ("red", "green", "blue")
single = (42,)          # ⚠️ Dấu phẩy bắt buộc cho tuple 1 phần tử
not_tuple = (42)        # Đây là int 42, KHÔNG phải tuple!
empty = ()

# Truy cập — giống List
print(point[0])         # 3
print(colors[-1])       # blue
print(colors[1:])       # ('green', 'blue')

# Immutable — không thể sửa
# colors[0] = "yellow"  # TypeError: 'tuple' object does not support item assignment

# Tuple packing / unpacking — rất hay dùng
x, y = point            # Unpacking — Java: x = point[0]; y = point[1]
print(x, y)             # 3 7

# Swap không cần biến tạm — đặc trưng Python
a, b = 10, 20
a, b = b, a             # Java: temp = a; a = b; b = temp;
print(a, b)             # 20 10

# Unpacking với *
first, *rest = [1, 2, 3, 4, 5]
print(first)    # 1
print(rest)     # [2, 3, 4, 5]

*init, last = [1, 2, 3, 4, 5]
print(init)     # [1, 2, 3, 4]
print(last)     # 5
```

### 3.2 Khi Nào Nên Dùng Tuple?

| Trường hợp                        | Dùng Tuple                  | Dùng List            |
|-----------------------------------|-----------------------------|----------------------|
| Tọa độ, màu sắc, cấu hình cố định | ✅ Immutable, an toàn        | ❌                    |
| Key của Dictionary                | ✅ Tuple có thể làm key      | ❌ List không thể     |
| Return nhiều giá trị từ hàm       | ✅ Pattern phổ biến          | Có thể dùng          |
| Dữ liệu cần thêm/bớt             | ❌                            | ✅                    |

```python
# Tuple làm key của Dict — List không làm được
locations = {}
locations[(10, 20)] = "Điểm A"    # Tuple key OK
locations[(30, 40)] = "Điểm B"
# locations[[10, 20]] = "X"       # TypeError: unhashable type: 'list'

# Return nhiều giá trị từ hàm
def get_min_max(numbers):
    return min(numbers), max(numbers)   # Trả về tuple

low, high = get_min_max([3, 1, 4, 1, 5, 9])
print(f"Min: {low}, Max: {high}")   # Min: 1, Max: 9
```

---

## 4. Set — Tập Hợp Không Trùng Lặp

### 4.1 Tìm Hiểu Set

> **Java developer:** Set Python tương tự `HashSet<T>` — không có thứ tự, không trùng lặp.

```python
# Khởi tạo
fruits = {"apple", "banana", "cherry", "apple"}  # Trùng lặp bị loại
print(fruits)   # {'cherry', 'banana', 'apple'} — thứ tự không đảm bảo

empty_set = set()   # ⚠️ {} tạo dict rỗng, KHÔNG phải set rỗng

# Từ list — loại bỏ trùng lặp
numbers = [1, 2, 2, 3, 3, 3, 4]
unique = set(numbers)
print(unique)   # {1, 2, 3, 4}

# Thêm / xóa
s = {1, 2, 3}
s.add(4)            # Java: set.add(4)
s.discard(2)        # Xóa, không ném lỗi nếu không tồn tại
s.remove(3)         # Xóa, ném KeyError nếu không tồn tại
print(s)            # {1, 4}

# Kiểm tra thành viên
print(4 in s)       # True — Java: set.contains(4)
```

### 4.2 Phép Hội, Giao, Hiệu

```python
A = {1, 2, 3, 4, 5}
B = {4, 5, 6, 7, 8}

# Phép hội (Union) — Java: A.addAll(B)
print(A | B)            # {1, 2, 3, 4, 5, 6, 7, 8}
print(A.union(B))       # Cách gọi method — kết quả giống nhau

# Phép giao (Intersection) — Java: A.retainAll(B)
print(A & B)            # {4, 5}
print(A.intersection(B))

# Phép hiệu (Difference) — phần tử có trong A nhưng không có trong B
print(A - B)            # {1, 2, 3}
print(A.difference(B))

# Hiệu đối xứng (Symmetric Difference) — phần tử thuộc A hoặc B nhưng không thuộc cả hai
print(A ^ B)                        # {1, 2, 3, 6, 7, 8}
print(A.symmetric_difference(B))

# Kiểm tra quan hệ tập hợp
C = {1, 2}
print(C.issubset(A))    # True — C ⊆ A — Java: A.containsAll(C)
print(A.issuperset(C))  # True — A ⊇ C
print(A.isdisjoint(B))  # False — A ∩ B ≠ ∅ (có phần tử chung)
```

```
Sơ đồ các phép toán:
  A = {1,2,3,4,5}    B = {4,5,6,7,8}

  A | B  = {1,2,3,4,5,6,7,8}  — tất cả
  A & B  = {4,5}               — chỉ phần chung
  A - B  = {1,2,3}             — A trừ đi phần chung
  A ^ B  = {1,2,3,6,7,8}      — không kể phần chung
```

---

## 5. Dictionary — Từ Điển Key-Value

### 5.1 Khởi Tạo, Truy Cập, Cập Nhật

> **Java developer:** Dictionary Python tương tự `HashMap<K, V>` nhưng từ Python 3.7+ giữ **thứ tự chèn vào** (Java's `LinkedHashMap`).

```python
# Khởi tạo
user = {
    "name": "Hoàng",
    "age": 28,
    "city": "Ho Chi Minh"
}

# Khởi tạo từ danh sách cặp key-value
config = dict(host="localhost", port=8080, debug=True)
print(config)   # {'host': 'localhost', 'port': 8080, 'debug': True}

empty = {}      # Dict rỗng

# Truy cập
print(user["name"])         # "Hoàng" — Java: map.get("name")
# print(user["email"])      # KeyError nếu key không tồn tại

# Cập nhật / thêm key
user["email"] = "hoang@example.com"  # Java: map.put("email", ...)
user["age"] = 29                      # Ghi đè giá trị
print(user)

# Xóa
del user["city"]                # Java: map.remove("city")
removed = user.pop("age")       # Xóa và trả về giá trị
print(removed)                  # 29
```

### 5.2 Các Phương Thức Quan Trọng

```python
product = {
    "id": 1,
    "name": "Laptop",
    "price": 25_000_000,
    "stock": 10
}

# .keys() — danh sách key — Java: map.keySet()
print(product.keys())           # dict_keys(['id', 'name', 'price', 'stock'])
print(list(product.keys()))     # ['id', 'name', 'price', 'stock']

# .values() — danh sách giá trị — Java: map.values()
print(list(product.values()))   # [1, 'Laptop', 25000000, 10]

# .items() — danh sách cặp (key, value) — Java: map.entrySet()
for key, value in product.items():
    print(f"{key}: {value}")
```

```python
# .get() — truy cập an toàn, không ném KeyError
# Java: map.getOrDefault("discount", 0)
print(product.get("discount"))          # None — không có KeyError
print(product.get("discount", 0))       # 0   — giá trị mặc định

# .setdefault() — lấy giá trị hoặc đặt giá trị mặc định nếu key chưa tồn tại
product.setdefault("discount", 0)
print(product["discount"])  # 0 — đã được đặt
product.setdefault("price", 99999)
print(product["price"])     # 25_000_000 — giữ nguyên vì key đã tồn tại

# .update() — merge dict — Java: map.putAll(other)
extra_info = {"brand": "Dell", "warranty": 2}
product.update(extra_info)
print(product)

# Python 3.9+ — merge operator |
merged = product | {"color": "black"}
print(merged)

# Dict comprehension — tạo dict nhanh
prices = {"apple": 10000, "banana": 5000, "cherry": 15000}
discounted = {k: int(v * 0.9) for k, v in prices.items()}
print(discounted)   # {'apple': 9000, 'banana': 4500, 'cherry': 13500}
```

### 5.3 Pattern Thường Gặp Với Dictionary

```python
# Đếm tần suất
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]

freq = {}
for word in words:
    freq[word] = freq.get(word, 0) + 1
print(freq)         # {'apple': 3, 'banana': 2, 'cherry': 1}

# Dùng collections.Counter — tiện hơn
from collections import Counter
freq2 = Counter(words)
print(freq2)        # Counter({'apple': 3, 'banana': 2, 'cherry': 1})

# Nhóm theo điều kiện (grouping)
students = [
    {"name": "Alice", "grade": "A"},
    {"name": "Bob", "grade": "B"},
    {"name": "Charlie", "grade": "A"},
    {"name": "Dave", "grade": "B"},
]

grouped = {}
for s in students:
    grade = s["grade"]
    grouped.setdefault(grade, []).append(s["name"])
print(grouped)  # {'A': ['Alice', 'Charlie'], 'B': ['Bob', 'Dave']}
```

---

## Tóm Tắt — So Sánh Nhanh Java vs Python

| Cấu trúc dữ liệu | Java                   | Python              | Ghi chú                              |
|------------------|------------------------|---------------------|--------------------------------------|
| String           | `String`               | `str`               | Đều immutable                        |
| Cắt chuỗi        | `substring(a, b)`      | `s[a:b]`            | Python hỗ trợ chỉ số âm              |
| Đảo chuỗi        | `StringBuilder.reverse()` | `s[::-1]`        | Python ngắn hơn nhiều                |
| Format string    | `String.format()`      | f-string            | f-string ngắn gọn hơn                |
| Danh sách        | `ArrayList<T>`         | `list`              | Python: nhiều kiểu cùng lúc          |
| Slicing list     | `subList(a, b)`        | `lst[a:b]`          | Python hỗ trợ step                   |
| Thêm cuối        | `list.add(x)`          | `list.append(x)`    | —                                    |
| Nối list         | `list.addAll(other)`   | `list.extend(other)` | —                                   |
| Xóa theo giá trị | `list.remove(val)`    | `list.remove(val)`  | Giống nhau                           |
| Danh sách bất biến | `List.of(...)`       | `tuple`             | Tuple làm key dict được              |
| Tập hợp          | `HashSet<T>`           | `set`               | Python có toán tử `|`, `&`, `-`, `^` |
| Map/Dict         | `HashMap<K,V>`         | `dict`              | Python 3.7+ giữ thứ tự chèn          |
| Lấy hoặc default | `getOrDefault(k, v)`  | `dict.get(k, v)`    | —                                    |
| Duyệt key-value  | `entrySet()`           | `.items()`          | —                                    |

---

## Bài Tập Thực Hành

Tạo file `practice_04.py` và viết code cho các bài sau:

```python
# Bài 1: Xử lý String
# Cho chuỗi: "  Python FastAPI Backend Development  "
# a) Xóa khoảng trắng hai đầu, viết hoa chữ cái đầu mỗi từ
# b) Đếm số từ trong chuỗi
# c) Đảo ngược chuỗi (sau khi đã strip)
# d) Kiểm tra chuỗi có chứa "FastAPI" không

text = "  Python FastAPI Backend Development  "
cleaned = text.strip().title()
print(cleaned)
print(f"Số từ: {len(cleaned.split())}")
print(f"Đảo ngược: {cleaned[::-1]}")
print(f"Có FastAPI: {'FastAPI' in cleaned}")


# Bài 2: Xử lý CSV đơn giản với split/join
csv_data = "id,name,age,city\n1,Alice,25,HCM\n2,Bob,30,HN\n3,Charlie,22,DN"

lines = csv_data.strip().split("\n")
header = lines[0].split(",")
records = [dict(zip(header, line.split(","))) for line in lines[1:]]

for record in records:
    print(f"{record['name']} ({record['age']} tuổi) — {record['city']}")


# Bài 3: Thao tác List
# Cho danh sách điểm, tìm: top 3, điểm trung bình, điểm trên trung bình
scores = [85, 42, 91, 33, 78, 55, 20, 67, 95, 60]

top3 = sorted(scores, reverse=True)[:3]
average = sum(scores) / len(scores)
above_avg = [s for s in scores if s > average]

print(f"Top 3: {top3}")
print(f"Trung bình: {average:.1f}")
print(f"Trên trung bình: {above_avg}")


# Bài 4: Stack và Queue
# a) Dùng Stack kiểm tra chuỗi dấu ngoặc có hợp lệ không
def is_valid_brackets(s):
    stack = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return len(stack) == 0

print(is_valid_brackets("({[]})"))     # True
print(is_valid_brackets("({[})"))      # False


# Bài 5: Set — tìm phần tử chung và khác biệt
team_a = {"Alice", "Bob", "Charlie", "Dave"}
team_b = {"Charlie", "Dave", "Eve", "Frank"}

print(f"Cả hai team: {team_a & team_b}")
print(f"Chỉ team A: {team_a - team_b}")
print(f"Tất cả thành viên: {team_a | team_b}")
print(f"Chỉ ở một team: {team_a ^ team_b}")


# Bài 6: Dictionary — thống kê từ văn bản
paragraph = """python is a great language python is easy to learn
fastapi is built on python fastapi is fast and easy to use"""

words = paragraph.split()
word_count = {}
for word in words:
    word_count[word] = word_count.get(word, 0) + 1

# Sắp xếp theo tần suất giảm dần
sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
print("Top 5 từ xuất hiện nhiều nhất:")
for word, count in sorted_words[:5]:
    print(f"  {word}: {count} lần")
```
