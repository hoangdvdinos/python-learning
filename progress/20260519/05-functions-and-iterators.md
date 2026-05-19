# 05 — Hàm & Iterator

> **Khối 4 — Hàm & Iterator**
> Dành cho Java developer — tập trung vào điểm khác biệt so với Java.

---

## 1. Xây Dựng Hàm Trong Python

### 1.1 Cú Pháp Cơ Bản

> **Java developer chú ý:** Python dùng từ khóa `def` thay vì khai báo kiểu trả về. Không có `void` — hàm không return tường minh sẽ trả về `None`.

```python
# Java:
# public int add(int a, int b) {
#     return a + b;
# }

# Python:
def add(a, b):
    return a + b

result = add(3, 5)
print(result)   # 8

# Hàm không return tường minh → trả về None (giống void Java)
def greet(name):
    print(f"Xin chào {name}!")

value = greet("Hoàng")
print(value)    # None
```

### 1.2 Return Nhiều Giá Trị

> **Java không có** — phải dùng Object, Map, hay custom class. Python return tuple ngầm định.

```python
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

low, high, avg = get_stats([3, 1, 4, 1, 5, 9, 2, 6])
print(f"Min: {low}, Max: {high}, Avg: {avg:.2f}")
# Min: 1, Max: 9, Avg: 3.88

# Thực chất là trả về tuple
result = get_stats([3, 1, 4, 1, 5, 9, 2, 6])
print(type(result))     # <class 'tuple'>
print(result)           # (1, 9, 3.875)
```

---

## 2. Tham Số Hàm: Positional, Keyword, Default Value

### 2.1 Positional và Keyword Arguments

```python
def describe_product(name, price, stock):
    print(f"{name}: {price:,} VND (còn {stock} cái)")

# Positional — theo thứ tự (giống Java)
describe_product("Laptop", 25_000_000, 10)

# Keyword — gọi theo tên, thứ tự tùy ý
describe_product(price=25_000_000, stock=10, name="Laptop")

# Trộn — positional trước, keyword sau
describe_product("Laptop", stock=10, price=25_000_000)
```

### 2.2 Default Value

```python
# Java: không có default value tường minh → phải overload method
# Python: gán giá trị mặc định ngay trong khai báo

def create_user(name, role="user", is_active=True):
    return {"name": name, "role": role, "is_active": is_active}

# Chỉ truyền tham số bắt buộc
u1 = create_user("Alice")
print(u1)   # {'name': 'Alice', 'role': 'user', 'is_active': True}

# Ghi đè một số tham số
u2 = create_user("Bob", role="admin")
print(u2)   # {'name': 'Bob', 'role': 'admin', 'is_active': True}
```

> **⚠️ Bẫy phổ biến — Mutable Default Value:**

```python
# SAI — list dùng chung cho mọi lần gọi hàm
def add_item_bad(item, items=[]):
    items.append(item)
    return items

print(add_item_bad("a"))    # ['a']
print(add_item_bad("b"))    # ['a', 'b']  ← bị "nhiễm" từ lần gọi trước!

# ĐÚNG — dùng None làm sentinel
def add_item_good(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

print(add_item_good("a"))   # ['a']
print(add_item_good("b"))   # ['b']  ← sạch
```

### 2.3 Positional-Only và Keyword-Only Parameters

```python
# Keyword-only: tham số sau * bắt buộc phải gọi bằng tên
def connect(host, port, *, timeout=30, retry=3):
    print(f"Kết nối {host}:{port}, timeout={timeout}s, retry={retry}")

connect("localhost", 5432, timeout=60)      # OK
# connect("localhost", 5432, 60)            # TypeError — timeout phải là keyword

# Positional-only (Python 3.8+): tham số trước / chỉ nhận theo vị trí
def normalize(value, /, min_val=0, max_val=1):
    return (value - min_val) / (max_val - min_val)

normalize(0.5)                  # OK
# normalize(value=0.5)          # TypeError — value chỉ được truyền positional
```

---

## 3. `*args` và `**kwargs`

### 3.1 `*args` — Nhận Số Lượng Đối Số Tùy Ý

> **Java tương đương:** `void method(String... args)` — varargs.

```python
# *args thu gom tất cả positional arguments vào tuple
def sum_all(*numbers):
    print(type(numbers))    # <class 'tuple'>
    return sum(numbers)

print(sum_all(1, 2, 3))         # 6
print(sum_all(1, 2, 3, 4, 5))  # 15
print(sum_all())                # 0

# Kết hợp tham số thường với *args
def log(level, *messages):
    for msg in messages:
        print(f"[{level}] {msg}")

log("INFO", "Server started", "Listening on port 8080")
# [INFO] Server started
# [INFO] Listening on port 8080
```

```python
# Unpacking với * khi gọi hàm
def add(a, b, c):
    return a + b + c

values = [1, 2, 3]
print(add(*values))     # 6 — giải nén list thành positional args
```

### 3.2 `**kwargs` — Nhận Keyword Arguments Tùy Ý

> **Java tương đương:** `Map<String, Object>` — nhưng Python làm tự động.

```python
# **kwargs thu gom tất cả keyword arguments vào dict
def print_info(**details):
    print(type(details))    # <class 'dict'>
    for key, value in details.items():
        print(f"  {key}: {value}")

print_info(name="Hoàng", age=28, city="HCM")
# name: Hoàng
# age: 28
# city: HCM

# Ứng dụng: build query filter linh hoạt
def build_query(table, **filters):
    conditions = " AND ".join(f"{k} = '{v}'" for k, v in filters.items())
    return f"SELECT * FROM {table} WHERE {conditions}"

q = build_query("users", role="admin", is_active=True)
print(q)    # SELECT * FROM users WHERE role = 'admin' AND is_active = 'True'
```

```python
# Unpacking với ** khi gọi hàm
def create_user(name, role, is_active):
    return {"name": name, "role": role, "is_active": is_active}

data = {"name": "Alice", "role": "admin", "is_active": True}
user = create_user(**data)  # Giải nén dict thành keyword args
print(user)
```

### 3.3 Thứ Tự Tham Số Chuẩn

```python
# Thứ tự bắt buộc: positional → *args → keyword-only → **kwargs
def full_example(pos1, pos2, *args, kw_only=0, **kwargs):
    print(f"pos: {pos1}, {pos2}")
    print(f"args: {args}")
    print(f"kw_only: {kw_only}")
    print(f"kwargs: {kwargs}")

full_example(1, 2, 3, 4, 5, kw_only=99, extra="hello", flag=True)
# pos: 1, 2
# args: (3, 4, 5)
# kw_only: 99
# kwargs: {'extra': 'hello', 'flag': True}
```

| Loại         | Ký hiệu    | Kết quả       | Java tương đương           |
|--------------|------------|---------------|----------------------------|
| Positional   | `a, b`     | Giá trị đơn   | Tham số thông thường       |
| *args        | `*args`    | `tuple`       | `Type... args` (varargs)   |
| **kwargs     | `**kwargs` | `dict`        | `Map<String, Object>`      |
| Keyword-only | `*, kw`    | Giá trị đơn   | Không có (phải tự kiểm tra) |

---

## 4. Hàm Lambda (Anonymous Function)

### 4.1 Cú Pháp

> **Java tương đương:** Lambda expression `(a, b) -> a + b`.

```python
# Java: BinaryOperator<Integer> add = (a, b) -> a + b;
# Python:
add = lambda a, b: a + b
print(add(3, 5))    # 8

# Lambda chỉ được phép một expression — không có statement, không có return
square = lambda x: x ** 2
is_even = lambda n: n % 2 == 0
greet = lambda name: f"Xin chào {name}!"
```

### 4.2 Ứng Dụng Thực Tế

Lambda thường dùng làm argument cho các hàm bậc cao — không cần đặt tên.

```python
products = [
    {"name": "Laptop", "price": 25_000_000},
    {"name": "Mouse", "price": 300_000},
    {"name": "Keyboard", "price": 800_000},
    {"name": "Monitor", "price": 8_000_000},
]

# Sắp xếp theo price — Java: list.sort(Comparator.comparing(p -> p.getPrice()))
products.sort(key=lambda p: p["price"])
for p in products:
    print(f"{p['name']}: {p['price']:,}")
# Mouse: 300,000
# Keyboard: 800,000
# Monitor: 8,000,000
# Laptop: 25,000,000

# Sắp xếp theo name, sau đó price (multi-key sort)
products.sort(key=lambda p: (len(p["name"]), p["price"]))

# Lọc
expensive = list(filter(lambda p: p["price"] >= 1_000_000, products))
```

> **Khi nào dùng lambda?** Khi logic đơn giản và chỉ dùng một lần. Nếu phức tạp hơn, hãy dùng `def` bình thường để dễ đọc hơn.

---

## 5. Các Hàm Built-in Quan Trọng

### 5.1 `map` — Áp Dụng Hàm Lên Toàn Bộ Iterable

> **Java tương đương:** `.stream().map(...)` trong Stream API.

```python
numbers = [1, 2, 3, 4, 5]

# map(function, iterable) → trả về map object (lazy)
squares = map(lambda n: n ** 2, numbers)
print(list(squares))    # [1, 4, 9, 16, 25]

# Dùng hàm có tên thay lambda
def to_usd(vnd):
    return round(vnd / 25_000, 2)

prices_vnd = [25_000_000, 300_000, 8_000_000]
prices_usd = list(map(to_usd, prices_vnd))
print(prices_usd)   # [1000.0, 12.0, 320.0]

# map với nhiều iterable
a = [1, 2, 3]
b = [10, 20, 30]
totals = list(map(lambda x, y: x + y, a, b))
print(totals)       # [11, 22, 33]
```

> **Lưu ý:** Trong Python hiện đại, **list comprehension thường được ưu tiên** hơn `map` vì dễ đọc hơn:
> `[n**2 for n in numbers]` rõ hơn `list(map(lambda n: n**2, numbers))`

### 5.2 `filter` — Lọc Phần Tử Theo Điều Kiện

> **Java tương đương:** `.stream().filter(...)`

```python
numbers = [1, -2, 3, -4, 5, -6, 7]

# filter(predicate, iterable) → trả về filter object (lazy)
positives = list(filter(lambda n: n > 0, numbers))
print(positives)    # [1, 3, 5, 7]

# filter với None — loại bỏ falsy values
mixed = [0, 1, "", "hello", None, True, False, [], [1, 2]]
truthy = list(filter(None, mixed))
print(truthy)       # [1, 'hello', True, [1, 2]]

# Tương đương comprehension — thường ưu tiên hơn
positives_comp = [n for n in numbers if n > 0]
```

### 5.3 `sorted` — Sắp Xếp Linh Hoạt

```python
# sorted() — trả về list mới (không sửa gốc)
# .sort()  — sắp xếp tại chỗ (in-place), chỉ dùng cho list

numbers = [3, 1, 4, 1, 5, 9, 2, 6]

asc = sorted(numbers)           # [1, 1, 2, 3, 4, 5, 6, 9]
desc = sorted(numbers, reverse=True)    # [9, 6, 5, 4, 3, 2, 1, 1]

# key= — sắp xếp theo tiêu chí tùy chỉnh
words = ["banana", "apple", "cherry", "fig", "date"]
by_length = sorted(words, key=len)
print(by_length)    # ['fig', 'date', 'apple', 'banana', 'cherry']

# Sắp xếp không phân biệt hoa thường
names = ["Bob", "alice", "Charlie", "dave"]
print(sorted(names, key=str.lower))     # ['alice', 'Bob', 'Charlie', 'dave']

# Multi-key sort với tuple
students = [
    ("Alice", 85), ("Bob", 92), ("Charlie", 85), ("Dave", 70)
]
# Sắp xếp theo điểm giảm dần, sau đó tên tăng dần
ranked = sorted(students, key=lambda s: (-s[1], s[0]))
print(ranked)
# [('Bob', 92), ('Alice', 85), ('Charlie', 85), ('Dave', 70)]
```

### 5.4 `enumerate` và `zip`

```python
# enumerate — đã học ở Khối 2, ôn lại nhanh
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")

# zip — ghép nhiều iterable thành cặp
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]
cities = ["HCM", "HN", "DN"]

# zip dừng khi iterable ngắn nhất kết thúc
for name, score, city in zip(names, scores, cities):
    print(f"{name} ({city}): {score} điểm")
# Alice (HCM): 85 điểm
# Bob (HN): 92 điểm
# Charlie (DN): 78 điểm

# Tạo dict từ hai list bằng zip
keys = ["name", "age", "city"]
values = ["Hoàng", 28, "HCM"]
user = dict(zip(keys, values))
print(user)     # {'name': 'Hoàng', 'age': 28, 'city': 'HCM'}

# zip_longest — ghép đến list dài nhất (dùng itertools)
from itertools import zip_longest
a = [1, 2, 3]
b = ["a", "b"]
pairs = list(zip_longest(a, b, fillvalue=None))
print(pairs)    # [(1, 'a'), (2, 'b'), (3, None)]
```

---

## 6. Scope Biến: Local, Global, Nonlocal

### 6.1 LEGB Rule

> Python tìm biến theo thứ tự: **L**ocal → **E**nclosing → **G**lobal → **B**uilt-in.

```python
x = "global"        # Global scope

def outer():
    x = "enclosing" # Enclosing scope

    def inner():
        x = "local" # Local scope
        print(x)    # local — tìm thấy ở Local trước
    inner()
    print(x)        # enclosing

outer()
print(x)            # global
```

### 6.2 `global` — Sửa Biến Global Từ Trong Hàm

```python
counter = 0

def increment():
    global counter      # Khai báo muốn sửa biến global
    counter += 1

increment()
increment()
print(counter)  # 2

# Không có global — Python tạo biến local mới
def increment_wrong():
    counter += 1    # UnboundLocalError — Python thấy có phép gán nên coi là local
                    # nhưng local chưa được khởi tạo trước khi += 1
```

> **Lưu ý:** Dùng `global` quá nhiều là code smell — thay bằng class hoặc truyền/trả về giá trị.

### 6.3 `nonlocal` — Sửa Biến Của Hàm Ngoài Bao Quanh

```python
# nonlocal — tương tự global nhưng cho enclosing scope (không phải global)
# Không có tương đương trong Java

def make_counter():
    count = 0

    def increment():
        nonlocal count  # Sửa biến count của make_counter
        count += 1
        return count

    return increment    # Trả về hàm — closure!

counter1 = make_counter()
counter2 = make_counter()   # Closure riêng biệt — count độc lập

print(counter1())   # 1
print(counter1())   # 2
print(counter1())   # 3
print(counter2())   # 1 — bắt đầu từ 0 riêng
```

| Từ khóa   | Phạm vi tác động            | Java tương đương     |
|-----------|-----------------------------|-----------------------|
| (không có) | Đọc từ outer scope được, nhưng ghi tạo local mới | (mặc định Java) |
| `global`  | Sửa biến ở module scope     | `static` field        |
| `nonlocal` | Sửa biến của hàm ngoài bao quanh | Không có         |

---

## 7. Iterator và Giao Thức `__iter__` / `__next__`

### 7.1 Iterable vs Iterator

> **Java developer:** Tương tự `Iterable<T>` và `Iterator<T>` trong Java Collections.

```python
# Iterable — đối tượng có thể duyệt được (có __iter__)
# Iterator — đối tượng giữ trạng thái duyệt (có __iter__ + __next__)

my_list = [1, 2, 3]    # Iterable

# Lấy iterator từ iterable
it = iter(my_list)     # Gọi my_list.__iter__()
print(type(it))        # <class 'list_iterator'>

print(next(it))        # 1 — Gọi it.__next__()
print(next(it))        # 2
print(next(it))        # 3
# next(it)             # StopIteration — hết phần tử

# for loop thực chất làm điều này tự động
for item in my_list:   # Python gọi iter() → next() liên tục cho đến StopIteration
    print(item)
```

### 7.2 Tự Xây Dựng Iterator

```python
class CountDown:
    """Iterator đếm ngược từ start về 0."""

    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self         # Iterator tự trả về chính nó

    def __next__(self):
        if self.current < 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

# Dùng trong for loop
for n in CountDown(5):
    print(n, end=" ")   # 5 4 3 2 1 0

# Dùng với next() thủ công
cd = CountDown(3)
print(next(cd))     # 3
print(next(cd))     # 2
```

---

## 8. Generator Function và `yield`

### 8.1 Tại Sao Cần Generator?

> Generator giải quyết vấn đề tạo dữ liệu lớn mà không cần lưu toàn bộ vào bộ nhớ. **Java không có** cú pháp tương đương trực tiếp (gần nhất là Stream API).

```python
# Cách thông thường — tạo toàn bộ list trước
def get_squares_list(n):
    return [i ** 2 for i in range(n)]   # Lưu tất cả n phần tử vào RAM

# Generator — tạo từng phần tử khi cần
def get_squares_gen(n):
    for i in range(n):
        yield i ** 2    # Tạm dừng và trả về giá trị, nhớ trạng thái

# Nếu n = 1_000_000:
# get_squares_list(1_000_000) → ~8MB RAM
# get_squares_gen(1_000_000)  → ~200 bytes (chỉ lưu trạng thái)
```

### 8.2 Cơ Chế `yield`

```python
def simple_gen():
    print("Bắt đầu")
    yield 1             # Tạm dừng, trả về 1
    print("Sau yield 1")
    yield 2             # Tạm dừng, trả về 2
    print("Sau yield 2")
    yield 3
    print("Kết thúc")  # Chạy sau khi yield 3 được lấy

gen = simple_gen()
print(type(gen))        # <class 'generator'>

print(next(gen))        # "Bắt đầu" → 1
print(next(gen))        # "Sau yield 1" → 2
print(next(gen))        # "Sau yield 2" → 3
# next(gen)             # "Kết thúc" → StopIteration
```

### 8.3 Generator Expression

```python
# List comprehension → Generator expression: thay [] bằng ()
squares_list = [x ** 2 for x in range(1000000)]    # List — tạo ngay toàn bộ
squares_gen  = (x ** 2 for x in range(1000000))    # Generator — lazy

# Dùng trực tiếp trong sum, max, min — không cần chuyển sang list
total = sum(x ** 2 for x in range(1, 11))
print(total)    # 385

# Chuỗi generator pipeline — xử lý streaming
data = range(1, 1000001)
filtered = (n for n in data if n % 2 == 0)     # Chỉ số chẵn
squared  = (n ** 2 for n in filtered)           # Bình phương
result   = sum(n for n in squared if n < 1000) # Tổng những cái < 1000
print(result)   # Tính toàn bộ pipeline mà không cần lưu vào bộ nhớ
```

### 8.4 Ứng Dụng Thực Tế

```python
import os

# Generator đọc file lớn từng dòng — không load toàn bộ vào RAM
def read_large_file(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")

# Chỉ xử lý dòng chứa "ERROR" — không đọc toàn bộ file vào memory
# for line in read_large_file("app.log"):
#     if "ERROR" in line:
#         print(line)

# Generator cho dữ liệu phân trang (pagination)
def paginate(data, page_size):
    for i in range(0, len(data), page_size):
        yield data[i:i + page_size]

records = list(range(1, 26))    # 25 records
for page in paginate(records, page_size=10):
    print(f"Page: {page}")
# Page: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# Page: [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
# Page: [21, 22, 23, 24, 25]
```

---

## 9. Decorator Trong Python

### 9.1 Khái Niệm

> Decorator là hàm bọc bên ngoài hàm khác để thêm hành vi mà không sửa code gốc. **Java tương đương:** `@Aspect` trong AOP Spring, hoặc Proxy Pattern.

```python
# Hiểu rõ bằng cách không dùng @ trước
def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Gọi hàm: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[LOG] Hàm {func.__name__} kết thúc")
        return result
    return wrapper

def add(a, b):
    return a + b

# Bọc thủ công — không dùng @
logged_add = log_decorator(add)
print(logged_add(3, 5))
# [LOG] Gọi hàm: add
# [LOG] Hàm add kết thúc
# 8
```

### 9.2 Cú Pháp `@`

```python
# @ là cú pháp sugar cho: func = decorator(func)

def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Gọi: {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        print(f"[LOG] Trả về: {result}")
        return result
    return wrapper

@log_decorator
def multiply(a, b):
    return a * b

@log_decorator
def greet(name, greeting="Xin chào"):
    return f"{greeting}, {name}!"

print(multiply(4, 5))
# [LOG] Gọi: multiply((4, 5), {})
# [LOG] Trả về: 20
# 20

print(greet("Hoàng"))
# [LOG] Gọi: greet(('Hoàng',), {})
# [LOG] Trả về: Xin chào, Hoàng!
```

### 9.3 Decorator Với `functools.wraps`

```python
from functools import wraps
import time

# Không dùng wraps → mất metadata của hàm gốc
def timer(func):
    @wraps(func)    # Giữ nguyên __name__, __doc__ của hàm gốc
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[TIMER] {func.__name__} chạy trong {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_sum(n):
    """Tính tổng từ 1 đến n."""
    return sum(range(n + 1))

result = slow_sum(1_000_000)
print(result)
print(slow_sum.__name__)    # slow_sum (giữ tên gốc nhờ @wraps)
print(slow_sum.__doc__)     # Tính tổng từ 1 đến n.
```

### 9.4 Decorator Có Tham Số

```python
from functools import wraps

# Decorator nhận tham số → cần thêm một lớp hàm nữa
def retry(max_attempts=3, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"Lần {attempt}/{max_attempts} thất bại: {e}")
                    if attempt == max_attempts:
                        raise
        return wrapper
    return decorator

@retry(max_attempts=3, exceptions=(ValueError, ConnectionError))
def unstable_api_call(url):
    import random
    if random.random() < 0.7:
        raise ConnectionError("Timeout!")
    return f"Data from {url}"

# Dùng nhiều decorator cùng lúc — thứ tự áp dụng từ dưới lên
@timer
@retry(max_attempts=2)
def fetch_data():
    return "OK"
```

### 9.5 Các Decorator Có Sẵn Quan Trọng

```python
# @property — getter/setter kiểu Python (học kỹ hơn ở Khối 5 — OOP)
class Product:
    def __init__(self, price):
        self._price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Giá không thể âm")
        self._price = value

p = Product(100_000)
print(p.price)      # 100000 — gọi như attribute, không phải method
p.price = 200_000   # Gọi setter
# p.price = -1      # ValueError

# @staticmethod — phương thức không cần self (Java: static method)
# @classmethod   — phương thức nhận class thay vì instance
```

---

## Tóm Tắt — So Sánh Nhanh Java vs Python

| Chủ đề                     | Java                              | Python                                  |
|----------------------------|-----------------------------------|-----------------------------------------|
| Khai báo hàm               | `public ReturnType name(params)`  | `def name(params):`                     |
| Hàm không trả về           | `void`                            | Không khai báo (trả về `None`)          |
| Return nhiều giá trị       | Không trực tiếp (phải dùng class) | `return a, b, c` (tuple)               |
| Default parameter          | Không có (phải overload)          | `def f(x, y=10):`                      |
| Varargs                    | `Type... args`                    | `*args` (tuple)                         |
| Keyword varargs            | `Map<String, Object>`             | `**kwargs` (dict)                       |
| Lambda                     | `(a, b) -> a + b`                 | `lambda a, b: a + b`                   |
| Stream map                 | `.stream().map(...)`              | `map()` hoặc list comprehension         |
| Stream filter              | `.stream().filter(...)`           | `filter()` hoặc list comprehension      |
| Sort với key               | `Comparator.comparing(...)`       | `sorted(key=lambda ...)`               |
| Iterator interface         | `Iterable<T>` + `Iterator<T>`     | `__iter__` + `__next__`                 |
| Lazy sequence              | Stream API                        | Generator (`yield`)                     |
| AOP / Proxy                | `@Aspect`, Proxy pattern          | Decorator (`@`)                         |
| Global/static state        | `static` field                    | `global` (hạn chế dùng)               |
| Closure                    | Effectively final variable        | `nonlocal` + closure tự nhiên           |

---

## Bài Tập Thực Hành

Tạo file `practice_05.py` và viết code cho các bài sau:

```python
# ============================================================
# PHẦN 1 — Xây Dựng Hàm
# ============================================================

# Bài 1: Hàm với tham số linh hoạt
# Viết hàm tính trung bình, hỗ trợ:
# - Bỏ qua N phần tử lớn nhất và nhỏ nhất (trimmed mean)
# - Làm tròn đến số chữ số thập phân tùy chọn
def trimmed_mean(numbers, trim=0, decimal=2):
    sorted_nums = sorted(numbers)
    if trim > 0:
        sorted_nums = sorted_nums[trim:-trim]
    return round(sum(sorted_nums) / len(sorted_nums), decimal)

scores = [20, 85, 90, 92, 95, 98, 100]
print(trimmed_mean(scores))             # Trung bình thường
print(trimmed_mean(scores, trim=1))     # Bỏ 1 cao nhất và 1 thấp nhất
print(trimmed_mean(scores, trim=1, decimal=1))


# Bài 2: *args và **kwargs
# Viết hàm log linh hoạt:
# log("INFO", "Server started")
# log("ERROR", "DB failed", "Retry in 5s", host="db01", port=5432)
def log(level, *messages, **context):
    ctx = " | ".join(f"{k}={v}" for k, v in context.items())
    for msg in messages:
        print(f"[{level}] {msg}" + (f" ({ctx})" if ctx else ""))

log("INFO", "Server started", "Listening on port 8080")
log("ERROR", "DB failed", "Retry in 5s", host="db01", port=5432)


# Bài 3: Closure — bộ đếm độc lập
def make_counter(start=0, step=1):
    count = start

    def increment():
        nonlocal count
        count += step
        return count

    def reset():
        nonlocal count
        count = start

    def get():
        return count

    return increment, reset, get

inc, reset, get = make_counter(start=10, step=5)
print(inc())    # 15
print(inc())    # 20
print(inc())    # 25
reset()
print(get())    # 10


# ============================================================
# PHẦN 2 — Lambda, Built-in Functions, Generator, Decorator
# ============================================================

# Bài 4: Sắp xếp phức tạp với key
employees = [
    {"name": "Alice",   "dept": "Engineering", "salary": 35_000_000},
    {"name": "Bob",     "dept": "Marketing",   "salary": 28_000_000},
    {"name": "Charlie", "dept": "Engineering", "salary": 40_000_000},
    {"name": "Dave",    "dept": "Marketing",   "salary": 32_000_000},
    {"name": "Eve",     "dept": "Engineering", "salary": 35_000_000},
]

# a) Sắp xếp: dept tăng dần → salary giảm dần → name tăng dần
sorted_emp = sorted(employees, key=lambda e: (e["dept"], -e["salary"], e["name"]))
for e in sorted_emp:
    print(f"{e['dept']:15} | {e['name']:10} | {e['salary']:>12,}")

# b) Lấy top earner của mỗi phòng ban
from itertools import groupby
by_dept = sorted(employees, key=lambda e: e["dept"])
top_earners = {
    dept: max(list(group), key=lambda e: e["salary"])
    for dept, group in groupby(by_dept, key=lambda e: e["dept"])
}
for dept, emp in top_earners.items():
    print(f"Top {dept}: {emp['name']} ({emp['salary']:,})")


# Bài 5: Generator — đọc và xử lý dữ liệu lớn
def fibonacci():
    """Generator vô hạn dãy Fibonacci."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def take(n, gen):
    """Lấy n phần tử đầu từ generator."""
    for _ in range(n):
        yield next(gen)

fib = fibonacci()
print(list(take(10, fib)))   # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# Lấy các số Fibonacci chẵn nhỏ hơn 1000
fib2 = fibonacci()
even_fibs = list(
    n for n in take(30, fib2)
    if n % 2 == 0 and n < 1000
)
print(even_fibs)    # [0, 2, 8, 34, 144, 610]


# Bài 6: Decorator thực tế
from functools import wraps
import time

def validate_positive(*param_names):
    """Decorator kiểm tra các tham số phải dương."""
    def decorator(func):
        import inspect
        sig = inspect.signature(func)
        param_list = list(sig.parameters.keys())

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            for name in param_names:
                if name in bound.arguments and bound.arguments[name] <= 0:
                    raise ValueError(f"Tham số '{name}' phải là số dương, nhận: {bound.arguments[name]}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_positive("price", "quantity")
def calculate_total(price, quantity, discount=0):
    return price * quantity * (1 - discount)

print(calculate_total(100_000, 5))                  # 500000
print(calculate_total(100_000, 5, discount=0.1))    # 450000.0

try:
    calculate_total(-100, 5)    # ValueError
except ValueError as e:
    print(f"Lỗi: {e}")

try:
    calculate_total(100_000, 0) # ValueError
except ValueError as e:
    print(f"Lỗi: {e}")
```
