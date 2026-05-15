# 03 — Kiểm Soát Luồng (Flow Control)

> **Khối 2 — Kiểm Soát Luồng**
> Dành cho Java developer — tập trung vào điểm khác biệt so với Java.

---

## 1. Mệnh Đề Điều Kiện `if` / `elif` / `else`

### 1.1 Cú pháp cơ bản

> **Java developer chú ý:** Python dùng **indentation** (thụt lề) thay cho `{}`. Không có dấu `()` bắt buộc quanh điều kiện.

```python
# Java:
# if (score >= 90) {
#     System.out.println("A");
# } else if (score >= 70) {
#     System.out.println("B");
# } else {
#     System.out.println("F");
# }

# Python:
score = 85

if score >= 90:
    print("A")
elif score >= 70:       # Java: else if — Python: elif (viết tắt)
    print("B")
else:
    print("F")
```

| Đặc điểm          | Java                   | Python                        |
|--------------------|------------------------|-------------------------------|
| Mở khối            | `{`                    | `:` (dấu hai chấm)            |
| Đóng khối          | `}`                    | Hết indentation               |
| Else-if            | `else if`              | `elif`                        |
| Điều kiện          | `if (condition)`       | `if condition:` — không cần `()` |
| Switch-case        | `switch / case`        | Từ Python 3.10: `match / case` |

### 1.2 Điều kiện với Truthy / Falsy

```python
# Tận dụng truthy/falsy — pattern rất phổ biến trong Python
name = ""
items = []
user = None

if name:                  # Tương đương: if name != ""
    print(f"Xin chào {name}")

if not items:             # List rỗng → falsy
    print("Không có sản phẩm")

if user is None:          # Cách chuẩn kiểm tra None (tương tự Java: user == null)
    print("Chưa đăng nhập")
```

### 1.3 `match / case` — Switch-case của Python (3.10+)

```python
# Java:
# switch (status) {
#     case "pending": ... break;
#     case "active":  ... break;
#     default:        ...
# }

# Python 3.10+:
status = "active"

match status:
    case "pending":
        print("Đang chờ duyệt")
    case "active":
        print("Đang hoạt động")
    case "banned":
        print("Bị cấm")
    case _:             # _ là wildcard — tương tự default
        print("Trạng thái không xác định")
```

> `match/case` mạnh hơn Java's `switch` — có thể khớp với cấu trúc dữ liệu phức tạp (structural pattern matching). Khối này chỉ giới thiệu dạng cơ bản.

---

## 2. Vòng Lặp `while`

### 2.1 Cú pháp cơ bản

```python
# Java: while (condition) { ... }
# Python: while condition: — không có ()

count = 0

while count < 5:
    print(f"count = {count}")
    count += 1          # Python không có count++
```

### 2.2 Cơ chế dừng vòng lặp

```python
# Cách 1: Điều kiện trong while trở thành False
total = 0
n = 1
while n <= 100:
    total += n
    n += 1
print(f"Tổng 1..100 = {total}")   # 5050

# Cách 2: break — thoát ngay lập tức (giống Java)
secret = 42
guess = 0
attempts = 0

while True:             # Vòng lặp vô hạn — dừng bằng break
    guess = int(input("Đoán số: "))
    attempts += 1
    if guess == secret:
        print(f"Đúng! Đoán {attempts} lần")
        break
    elif guess < secret:
        print("Nhỏ hơn")
    else:
        print("Lớn hơn")
```

### 2.3 `while...else` — Python độc quyền

> **Java không có** cú pháp này. Khối `else` của `while` chạy khi vòng lặp kết thúc **tự nhiên** (điều kiện thành False), **không** chạy nếu thoát bằng `break`.

```python
# Tìm số nguyên tố — minh họa while...else
n = 17
divisor = 2

while divisor * divisor <= n:
    if n % divisor == 0:
        print(f"{n} không phải số nguyên tố (chia hết cho {divisor})")
        break
    divisor += 1
else:
    # Chỉ chạy nếu vòng lặp kết thúc mà không gặp break
    print(f"{n} là số nguyên tố")
```

---

## 3. Vòng Lặp `for` — Duyệt Phần Tử trong Container

### 3.1 `for` trong Python khác hoàn toàn Java

| Đặc điểm        | Java                           | Python                        |
|-----------------|--------------------------------|-------------------------------|
| Kiểu vòng lặp   | Index-based (`for (int i=0...`) | Iterator-based (for-each) |
| Cú pháp         | `for (Type item : collection)` | `for item in collection:`     |
| Không cần       | —                              | Không cần chỉ số `i` (thường) |
| For-each        | `for (String s : list)`        | `for s in list:`              |

```python
# Duyệt List — tương tự Java for-each
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)

# Duyệt String — Python string là iterable
for char in "Python":
    print(char)         # P y t h o n

# Duyệt Dict — duyệt theo key mặc định
user = {"name": "Hoang", "age": 25, "city": "HCM"}

for key in user:
    print(key)          # name, age, city

for key, value in user.items():   # Duyệt cả key lẫn value
    print(f"{key}: {value}")
```

### 3.2 `enumerate` — khi cần cả chỉ số lẫn giá trị

```python
# Java: for (int i = 0; i < fruits.size(); i++) { ... fruits.get(i) ... }
# Python — dùng enumerate()

fruits = ["apple", "banana", "cherry"]

for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
# 0: apple
# 1: banana
# 2: cherry

# Bắt đầu từ chỉ số khác 0
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")
# 1. apple
# 2. banana
# 3. cherry
```

### 3.3 `for...else` — Python độc quyền

```python
# Tương tự while...else — else chạy khi for kết thúc tự nhiên (không có break)

target = 7
numbers = [1, 3, 5, 9, 11]

for num in numbers:
    if num == target:
        print(f"Tìm thấy {target}")
        break
else:
    print(f"Không tìm thấy {target}")   # In ra dòng này
```

---

## 4. `continue` và `break`

### 4.1 `break` — thoát khỏi vòng lặp hiện tại

```python
# Giống Java — break thoát khỏi vòng lặp gần nhất
for i in range(10):
    if i == 5:
        break           # Dừng khi i = 5
    print(i)            # In 0, 1, 2, 3, 4
```

### 4.2 `continue` — bỏ qua iteration hiện tại

```python
# Giống Java — continue bỏ qua phần còn lại của vòng lặp hiện tại
for i in range(10):
    if i % 2 == 0:
        continue        # Bỏ qua số chẵn
    print(i)            # In 1, 3, 5, 7, 9
```

### 4.3 So sánh `break` vs `continue`

```python
numbers = [1, -2, 3, -4, 5, -6]

# break: dừng hẳn khi gặp số âm đầu tiên
print("=== break ===")
for n in numbers:
    if n < 0:
        break
    print(n)            # 1 (dừng khi gặp -2)

# continue: bỏ qua số âm, in số dương
print("=== continue ===")
for n in numbers:
    if n < 0:
        continue
    print(n)            # 1, 3, 5
```

### 4.4 Vòng lặp lồng nhau — `break` chỉ thoát vòng trong

> **Giống Java:** `break` chỉ thoát khỏi vòng lặp **gần nhất** bao quanh nó.

```python
# Java có label để break vòng ngoài — Python KHÔNG có label
# Python dùng flag variable hoặc refactor thành function

# Cách dùng flag:
found = False
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
target = 5

for row in matrix:
    for val in row:
        if val == target:
            found = True
            break       # Thoát vòng trong
    if found:
        break           # Thoát vòng ngoài
```

---

## 5. `range` — Xây Dựng Dãy Số

### 5.1 Cú pháp

```python
# range(stop)            → 0, 1, ..., stop-1
# range(start, stop)     → start, start+1, ..., stop-1
# range(start, stop, step) → start, start+step, ..., < stop
```

| Cách dùng              | Kết quả           | Java tương đương          |
|------------------------|-------------------|---------------------------|
| `range(5)`             | 0, 1, 2, 3, 4     | `for (int i=0; i<5; i++)` |
| `range(1, 6)`          | 1, 2, 3, 4, 5     | `for (int i=1; i<6; i++)` |
| `range(0, 10, 2)`      | 0, 2, 4, 6, 8     | `for (int i=0; i<10; i+=2)` |
| `range(10, 0, -1)`     | 10, 9, 8, ..., 1  | `for (int i=10; i>0; i--)` |

```python
# Đếm từ 0 đến 4
for i in range(5):
    print(i)        # 0 1 2 3 4

# Đếm từ 1 đến 10
for i in range(1, 11):
    print(i)        # 1 2 3 4 5 6 7 8 9 10

# Bước nhảy 2 — chỉ số chẵn
for i in range(0, 20, 2):
    print(i)        # 0 2 4 6 8 10 12 14 16 18

# Đếm ngược — Java: for (int i=5; i>0; i--)
for i in range(5, 0, -1):
    print(i)        # 5 4 3 2 1
```

### 5.2 `range` không phải List — đó là lazy sequence

```python
# range() không tạo sẵn list trong bộ nhớ — tiết kiệm RAM
r = range(1_000_000)
print(type(r))          # <class 'range'>
print(r[0], r[-1])      # 0  999999 — truy cập trực tiếp được

# Chuyển sang list khi cần thao tác list
nums = list(range(1, 6))    # [1, 2, 3, 4, 5]
```

---

## 6. Comprehension Expression

> **Không có trong Java** — đây là cú pháp đặc trưng và rất mạnh của Python. Tạo collection mới từ iterable trong **một dòng**.

### 6.1 List Comprehension

```python
# Cú pháp: [expression for item in iterable if condition]
#                                            ^^^^^^^^^^^^^ condition là tùy chọn

# Cách thông thường (Java style)
squares = []
for i in range(1, 6):
    squares.append(i ** 2)
print(squares)          # [1, 4, 9, 16, 25]

# List comprehension — cô đọng hơn
squares = [i ** 2 for i in range(1, 6)]
print(squares)          # [1, 4, 9, 16, 25]
```

```python
# Có điều kiện lọc
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Lấy số chẵn
evens = [n for n in numbers if n % 2 == 0]
print(evens)            # [2, 4, 6, 8, 10]

# Lấy bình phương của số lẻ
odd_squares = [n ** 2 for n in numbers if n % 2 != 0]
print(odd_squares)      # [1, 9, 25, 49, 81]
```

```python
# Biến đổi dữ liệu
names = ["  alice  ", "  bob  ", "  charlie  "]

# Xóa khoảng trắng và viết hoa
clean = [name.strip().title() for name in names]
print(clean)            # ['Alice', 'Bob', 'Charlie']

# Với Java Stream API: names.stream().map(String::trim).map(...)...collect(toList())
```

### 6.2 Dict Comprehension

```python
# Cú pháp: {key_expr: value_expr for item in iterable if condition}

# Tạo dict từ list
fruits = ["apple", "banana", "cherry"]
fruit_lengths = {fruit: len(fruit) for fruit in fruits}
print(fruit_lengths)    # {'apple': 5, 'banana': 6, 'cherry': 6}

# Đảo ngược dict (key ↔ value)
original = {"a": 1, "b": 2, "c": 3}
reversed_dict = {v: k for k, v in original.items()}
print(reversed_dict)    # {1: 'a', 2: 'b', 3: 'c'}

# Lọc theo điều kiện
scores = {"Alice": 85, "Bob": 42, "Charlie": 91, "Dave": 55}
passing = {name: score for name, score in scores.items() if score >= 60}
print(passing)          # {'Alice': 85, 'Charlie': 91}
```

### 6.3 Set Comprehension

```python
# Cú pháp: {expression for item in iterable if condition}
# Giống list comprehension nhưng dùng {} — kết quả là Set (không trùng lặp)

numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]

unique_squares = {n ** 2 for n in numbers}
print(unique_squares)   # {1, 4, 9, 16} — thứ tự không đảm bảo

# Ứng dụng: lấy tập ký tự duy nhất
sentence = "hello python"
unique_chars = {ch for ch in sentence if ch != " "}
print(unique_chars)     # {'h', 'e', 'l', 'o', 'p', 'y', 't', 'n'}
```

### 6.4 Tổng quan các loại Comprehension

| Loại              | Cú pháp                          | Kết quả    |
|-------------------|----------------------------------|------------|
| List comprehension | `[expr for x in it if cond]`    | `list`     |
| Dict comprehension | `{k: v for x in it if cond}`    | `dict`     |
| Set comprehension  | `{expr for x in it if cond}`    | `set`      |
| Generator expr     | `(expr for x in it if cond)`    | `generator` (lazy) |

---

## 7. Toán Tử Ba Ngôi (Ternary Operator)

### 7.1 Cú pháp

```python
# Java:  condition ? value_if_true : value_if_false
# Python: value_if_true if condition else value_if_false
#         ^^^^^^^^^^^^^ vế đúng đứng TRƯỚC condition

age = 20
label = "Người lớn" if age >= 18 else "Trẻ em"
print(label)            # Người lớn
```

> **⚠️ Điểm dễ nhầm:** Python đặt `value_if_true` **trước** `if`, ngược với Java đặt condition trước `?`.

### 7.2 Ứng dụng thực tế

```python
# Gán giá trị có điều kiện
x = 10
abs_x = x if x >= 0 else -x
print(abs_x)            # 10

# Trong f-string
score = 75
result = f"Đậu" if score >= 50 else "Rớt"
print(f"Kết quả: {result}")

# Gọi hàm khác nhau
def greet_formal(name):    return f"Kính chào {name}"
def greet_casual(name):    return f"Chào {name}!"

is_vip = True
name = "Hoàng"
greeting = greet_formal(name) if is_vip else greet_casual(name)
print(greeting)         # Kính chào Hoàng
```

### 7.3 Kết hợp với List Comprehension

```python
# Ternary bên trong comprehension — rất phổ biến
numbers = range(1, 11)

labels = ["chẵn" if n % 2 == 0 else "lẻ" for n in numbers]
print(labels)
# ['lẻ', 'chẵn', 'lẻ', 'chẵn', 'lẻ', 'chẵn', 'lẻ', 'chẵn', 'lẻ', 'chẵn']

# Biến đổi giá trị có điều kiện
prices = [100, -50, 200, -30, 150]
valid_prices = [p if p > 0 else 0 for p in prices]
print(valid_prices)     # [100, 0, 200, 0, 150]
```

### 7.4 Giới hạn — không nên lồng nhau

```python
# CÓ THỂ lồng nhau nhưng khó đọc — hạn chế dùng
score = 75
grade = "A" if score >= 90 else ("B" if score >= 80 else ("C" if score >= 70 else "F"))

# Nên dùng if/elif khi logic phức tạp
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
```

---

## Tóm Tắt — So Sánh Nhanh Java vs Python

| Chủ đề               | Java                          | Python                              |
|----------------------|-------------------------------|-------------------------------------|
| If-else              | `if (cond) { } else { }`     | `if cond:` + indentation            |
| Else-if              | `else if`                     | `elif`                              |
| Switch               | `switch/case`                 | `match/case` (3.10+)                |
| While                | `while (cond) { }`           | `while cond:`                       |
| While-else           | Không có                      | `while...else` (else khi không break) |
| For-each             | `for (T item : col)`          | `for item in col:`                  |
| For với index        | `for (int i=0; i<n; i++)`    | `for i in range(n):` hoặc `enumerate()` |
| For-else             | Không có                      | `for...else` (else khi không break) |
| Break                | `break`                       | `break` (giống)                     |
| Continue             | `continue`                    | `continue` (giống)                  |
| Break outer loop     | Label: `outer: break outer;`  | Dùng flag variable                  |
| Dãy số               | `IntStream.range(0, n)`       | `range(n)`                          |
| List từ range        | `IntStream.range(0,n).boxed().collect()` | `list(range(n))`        |
| List comprehension   | Stream API (dài hơn)          | `[expr for x in it]`                |
| Dict comprehension   | Không có                      | `{k: v for x in it}`               |
| Ternary              | `cond ? a : b`                | `a if cond else b`                  |

---

## Bài Tập Thực Hành

Tạo file `practice_03.py` và viết code cho các bài sau:

```python
# Bài 1: FizzBuzz kinh điển (for + range + ternary/if)
# In số 1-30. Chia hết 3 → "Fizz", chia hết 5 → "Buzz", cả hai → "FizzBuzz"
for i in range(1, 31):
    if i % 15 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)


# Bài 2: Tìm tất cả số nguyên tố từ 2 đến 50 (for + while/else hoặc for/else)
primes = []
for n in range(2, 51):
    for divisor in range(2, n):
        if n % divisor == 0:
            break
    else:
        primes.append(n)
print("Số nguyên tố:", primes)


# Bài 3: List comprehension — lọc và biến đổi
# Cho list điểm, tạo list mới: điểm >= 50 → "pass", < 50 → "fail"
scores = [85, 42, 91, 33, 78, 55, 20, 67]
results = ["pass" if s >= 50 else "fail" for s in scores]
print(results)

# Lấy chỉ các điểm đậu và nâng thêm 5 điểm (tối đa 100)
boosted = [min(s + 5, 100) for s in scores if s >= 50]
print(boosted)


# Bài 4: Dict comprehension — thống kê tần suất ký tự
text = "mississippi"
freq = {ch: text.count(ch) for ch in set(text)}
print(sorted(freq.items()))  # Sắp xếp để dễ đọc


# Bài 5: Tính tổng các số trong dãy Fibonacci nhỏ hơn 100
a, b = 0, 1
fib_sum = 0
while a < 100:
    fib_sum += a
    a, b = b, a + b     # Hoán đổi đồng thời — Python không cần biến tạm
print(f"Tổng Fibonacci < 100: {fib_sum}")


# Bài 6: Ma trận — for lồng nhau + comprehension
# Tạo bảng cửu chương 2x2 dạng dict
table = {(i, j): i * j for i in range(1, 4) for j in range(1, 4)}
for (i, j), val in table.items():
    print(f"{i} x {j} = {val}")
```
