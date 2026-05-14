# 02 — Kiểu Số, Boolean & Toán Tử

> **Khối 1 — Làm Quen Môi Trường & Kiểu Dữ Liệu Cơ Bản**
> Dành cho Java developer — tập trung vào điểm khác biệt so với Java.

---

## 1. Kiểu Số (Number Types)

### 1.1 Tổng quan

| Python   | Java tương đương       | Ghi chú                                      |
|----------|------------------------|----------------------------------------------|
| `int`    | `int`, `long`          | **Không giới hạn** độ lớn, không overflow    |
| `float`  | `double`               | 64-bit IEEE 754, không có `float` 32-bit     |
| `complex`| Không có sẵn           | Số phức `a + bj` — dùng trong tính toán khoa học |

> **Java dev chú ý:** Python không có `byte`, `short`, `long`, `float` (32-bit). Chỉ có `int` và `float`. `int` Python tự mở rộng bộ nhớ — không bao giờ overflow.

### 1.2 Khai báo

```python
# int — không giới hạn độ lớn
age = 30
big_number = 999_999_999_999_999_999_999  # Dấu _ để dễ đọc (Java cũng có)
hex_val = 0xFF                            # Hệ 16 (Java: 0xFF — giống)
bin_val = 0b1010                          # Hệ 2  (Java: 0b1010 — giống)

# float — tương đương double của Java
price = 19.99
scientific = 1.5e10   # 15_000_000_000.0

# complex — Python có sẵn, Java không có
z = 3 + 4j
print(z.real)   # 3.0
print(z.imag)   # 4.0
```

### 1.3 Phép toán số học

| Toán tử | Ý nghĩa         | Python              | Java                 |
|---------|-----------------|---------------------|----------------------|
| `+`     | Cộng            | `5 + 3` → `8`       | `5 + 3` → `8`        |
| `-`     | Trừ             | `5 - 3` → `2`       | `5 - 3` → `2`        |
| `*`     | Nhân            | `5 * 3` → `15`      | `5 * 3` → `15`       |
| `**`    | Lũy thừa        | `5 ** 3` → `125`    | `Math.pow(5, 3)`     |
| `/`     | Chia (luôn float) | `7 / 2` → `3.5`   | `7 / 2` → `3` ⚠️    |
| `//`    | Chia lấy nguyên | `7 // 2` → `3`      | `7 / 2` → `3`        |
| `%`     | Chia lấy dư     | `7 % 2` → `1`       | `7 % 2` → `1`        |

> **⚠️ Bẫy với Java dev:**
> - `7 / 2` trong Java → `3` (integer division)
> - `7 / 2` trong Python → `3.5` (luôn ra float!)
> - Muốn chia lấy nguyên như Java: dùng `//`

```python
# Minh họa
print(7 / 2)    # 3.5   ← Python: luôn float
print(7 // 2)   # 3     ← Python: floor division
print(7 % 2)    # 1
print(2 ** 10)  # 1024  ← thay cho Math.pow(2, 10)
```

### 1.4 Chuyển đổi kiểu (Type Conversion)

```python
# Java: (int) 3.9  →  Python: int(3.9)
x = int(3.9)       # 3 — cắt bỏ phần thập phân (không làm tròn)
y = float(5)       # 5.0
z = str(42)        # "42"
n = int("100")     # 100

# Kiểm tra kiểu — tương tự instanceof trong Java
print(type(42))          # <class 'int'>
print(isinstance(42, int))  # True
```

---

## 2. Kiểu Boolean

### 2.1 Khai báo

```python
# Java: boolean isActive = true;
# Python — chữ HOA chữ cái đầu
is_active = True
is_deleted = False
```

> **⚠️ Bẫy:** Java dùng `true`/`false` (chữ thường), Python dùng `True`/`False` (chữ HOA). Viết sai sẽ bị lỗi `NameError`.

### 2.2 Truthy & Falsy — Python linh hoạt hơn Java

Python tự động chuyển đổi nhiều giá trị sang `bool`. Java không làm vậy.

| Giá trị          | Python bool | Java bool   |
|------------------|-------------|-------------|
| `0`, `0.0`       | `False`     | Lỗi compile |
| `""`  (string rỗng) | `False`  | Lỗi compile |
| `[]`, `{}`, `()` | `False`     | Lỗi compile |
| `None`           | `False`     | Lỗi compile |
| Mọi giá trị khác | `True`      | —           |

```python
name = ""
if name:             # Tương đương: if name != "" and name is not None
    print("Có tên")
else:
    print("Tên rỗng")  # In ra dòng này

items = []
if not items:        # items rỗng → falsy → not items = True
    print("Danh sách trống")
```

### 2.3 `bool` là subclass của `int`

```python
# Đặc thù của Python — Java không có điều này
print(True + True)   # 2
print(True * 5)      # 5
print(False + 1)     # 1
print(int(True))     # 1
print(int(False))    # 0
```

---

## 3. Phép So Sánh & Toán Tử Logic

### 3.1 Phép so sánh

| Toán tử | Python       | Java         | Ghi chú                             |
|---------|--------------|--------------|-------------------------------------|
| `==`    | So sánh giá trị | So sánh giá trị (primitive) | Giống Java với primitive |
| `!=`    | Khác giá trị | `!=`         | —                                   |
| `>`     | Lớn hơn      | `>`          | —                                   |
| `<`     | Nhỏ hơn      | `<`          | —                                   |
| `>=`    | Lớn hơn hoặc bằng | `>=`   | —                                   |
| `<=`    | Nhỏ hơn hoặc bằng | `<=`   | —                                   |
| `is`    | So sánh **địa chỉ** | `==` với object | Tương tự `==` của Java với object |
| `is not`| Khác địa chỉ | `!=` với object | —                                |
| `in`    | Thuộc tập hợp | `.contains()` | Không có trong Java operator     |
| `not in`| Không thuộc  | `!.contains()` | —                                |

```python
# == so sánh giá trị
print(5 == 5)       # True
print("abc" == "abc")  # True

# Chained comparison — Java KHÔNG có
x = 5
print(1 < x < 10)   # True  (Java: 1 < x && x < 10)
print(1 < x < 4)    # False
```

### 3.2 `is` vs `==` — điểm dễ nhầm nhất

> **Java developer:** `==` trong Java so sánh địa chỉ với object, so sánh giá trị với primitive. Python tách biệt hoàn toàn: `==` luôn so sánh **giá trị**, `is` luôn so sánh **địa chỉ bộ nhớ**.

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a             # c trỏ vào cùng object với a

print(a == b)     # True  — cùng giá trị
print(a is b)     # False — khác địa chỉ (khác Java's == với object)
print(a is c)     # True  — cùng địa chỉ

# Dùng is chủ yếu để kiểm tra None — tương tự Java: obj == null
result = None
if result is None:      # Cách chuẩn trong Python
    print("Chưa có kết quả")

# Tránh dùng: if result == None — hoạt động nhưng không phải best practice
```

### 3.3 Toán tử `in`

```python
# Kiểm tra phần tử
numbers = [1, 2, 3, 4, 5]
print(3 in numbers)       # True  — Java: numbers.contains(3)
print(9 in numbers)       # False

# Với string — kiểm tra substring
message = "Hello, Python"
print("Python" in message)  # True  — Java: message.contains("Python")
print("Java" not in message) # True

# Với dict — kiểm tra key
config = {"host": "localhost", "port": 8080}
print("host" in config)   # True  — Java: config.containsKey("host")
```

### 3.4 Toán tử logic

| Python  | Java  | Ghi chú                              |
|---------|-------|--------------------------------------|
| `and`   | `&&`  | Trả về giá trị thực, không chỉ bool  |
| `or`    | `\|\|`  | Trả về giá trị thực, không chỉ bool  |
| `not`   | `!`   | Luôn trả về bool                     |

```python
# Cơ bản — giống Java
print(True and False)   # False
print(True or False)    # True
print(not True)         # False

# Short-circuit evaluation — giống Java
# and: nếu vế trái False → không tính vế phải
# or:  nếu vế trái True  → không tính vế phải
x = 0
if x != 0 and 10 / x > 1:   # Không lỗi ZeroDivisionError vì short-circuit
    print("OK")
```

> **Đặc thù Python:** `and`/`or` trả về **giá trị gốc**, không phải `True`/`False`. Java's `&&`/`||` luôn trả `boolean`.

```python
# and: trả về giá trị False đầu tiên, hoặc giá trị cuối nếu tất cả True
print(1 and 2)       # 2     (cả hai truthy → trả về cái cuối)
print(0 and 2)       # 0     (0 là falsy → trả về ngay)
print("" and "abc")  # ""    ("" là falsy → trả về ngay)

# or: trả về giá trị True đầu tiên, hoặc giá trị cuối nếu tất cả False
print(1 or 2)        # 1     (1 là truthy → trả về ngay)
print(0 or 2)        # 2     (0 falsy → kiểm tra tiếp, 2 truthy → trả về)
print(0 or "")       # ""    (cả hai falsy → trả về cái cuối)

# Ứng dụng thực tế — pattern hay dùng:
# Giá trị mặc định khi None (tương tự Java: value != null ? value : "default")
name = None
display_name = name or "Anonymous"   # "Anonymous"
print(display_name)
```

---

## 4. Phép Gán Kết Hợp (Assignment Operators)

### 4.1 Các toán tử

| Toán tử | Tương đương     | Java  | Ví dụ             |
|---------|-----------------|-------|-------------------|
| `+=`    | `x = x + n`    | `+=`  | `x += 5`          |
| `-=`    | `x = x - n`    | `-=`  | `x -= 3`          |
| `*=`    | `x = x * n`    | `*=`  | `x *= 2`          |
| `/=`    | `x = x / n`    | `/=`  | `x /= 4` → float! |
| `//=`   | `x = x // n`   | Không có | `x //= 2`      |
| `**=`   | `x = x ** n`   | Không có | `x **= 3`      |
| `%=`    | `x = x % n`    | `%=`  | `x %= 7`          |

```python
x = 10
x += 5    # x = 15  — giống Java
x -= 3    # x = 12  — giống Java
x *= 2    # x = 24  — giống Java

x /= 4    # x = 6.0 — ⚠️ Java: 24/4 = 6 (int), Python: 24/4 = 6.0 (float)
print(type(x))  # <class 'float'>

y = 10
y //= 3   # y = 3   — lấy nguyên (Java không có toán tử này)
y **= 2   # y = 9   — lũy thừa (Java không có)
y %= 4    # y = 1   — giống Java
```

### 4.2 Python KHÔNG có `++` và `--`

```python
# Java: i++, i--, ++i, --i
# Python: KHÔNG có — sẽ báo lỗi SyntaxError

counter = 0
counter += 1   # Cách Python — thay cho i++
counter -= 1   # Thay cho i--
```

> **Lý do:** Python không có `++`/`--` vì integer là **immutable object** — không thể tăng tại chỗ như Java.

---

## Tóm Tắt — So Sánh Nhanh Java vs Python

| Chủ đề              | Java                     | Python                        |
|---------------------|--------------------------|-------------------------------|
| Kiểu số nguyên      | `int`, `long`, `short`... | Chỉ `int` (không giới hạn)   |
| Chia lấy float      | Cần cast: `(double)7/2`  | `7/2` tự động → `3.5`        |
| Chia lấy nguyên     | `7/2` → `3`              | `7//2` → `3`                  |
| Lũy thừa            | `Math.pow(2, 10)`        | `2 ** 10`                     |
| Boolean literals    | `true`, `false`          | `True`, `False`               |
| Truthy/Falsy        | Không có                 | `0`, `""`, `[]`, `None` → False |
| So sánh địa chỉ     | `==` với object           | `is`                          |
| Kiểm tra null       | `obj == null`            | `obj is None`                 |
| Toán tử logic       | `&&`, `\|\|`, `!`           | `and`, `or`, `not`            |
| Kiểm tra membership | `.contains()`            | `in`, `not in`                |
| Tăng giảm 1         | `i++`, `i--`             | `i += 1`, `i -= 1`           |

---

## Bài Tập Thực Hành

Tạo file `practice_02.py` và viết code cho các bài sau:

```python
# Bài 1: Tính tiền sau thuế
price = 250_000
tax_rate = 0.1
total = price + price * tax_rate
print(f"Giá gốc: {price:,} VND")
print(f"Thuế: {price * tax_rate:,.0f} VND")
print(f"Tổng: {total:,.0f} VND")

# Bài 2: Kiểm tra năm nhuận (so sánh và logic)
year = 2024
is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
print(f"{year} {'là' if is_leap else 'không phải'} năm nhuận")

# Bài 3: Giá trị mặc định với or
user_input = ""
username = user_input or "guest"
print(f"Xin chào, {username}")

# Bài 4: Kiểm tra khoảng giá trị (chained comparison)
score = 85
grade = "A" if score >= 90 else "B" if 80 <= score < 90 else "C" if 70 <= score < 80 else "F"
print(f"Điểm {score} → Xếp loại {grade}")
```
