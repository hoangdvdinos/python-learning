# 07 — File, Module, Exception

> **Khối 6 — File, Module, Exception**
> Dành cho Java developer — tập trung vào điểm khác biệt so với Java.

---

## 1. Quy Trình Đọc File — `open()`, `with`, Các Chế Độ

### 1.1 Cú Pháp Cơ Bản

> **Java tương đương:** `FileReader` / `BufferedReader` / `try-with-resources`. Python dùng `with open(...)` — tương tự `try-with-resources`, tự động đóng file dù có exception hay không.

```python
# Java:
# try (BufferedReader br = new BufferedReader(new FileReader("file.txt"))) {
#     String line;
#     while ((line = br.readLine()) != null) { ... }
# }

# Python — luôn dùng with statement, không dùng open() trần
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()      # Đọc toàn bộ file thành một string
    print(content)
# File tự đóng khi ra khỏi with block — dù có exception

# Không dùng with — phải đóng thủ công (không khuyến khích)
f = open("file.txt", "r", encoding="utf-8")
try:
    content = f.read()
finally:
    f.close()   # Phải đảm bảo luôn đóng
```

### 1.2 Các Chế Độ Mở File

```python
# Chế độ text (mặc định)
open("file.txt", "r")    # Read  — đọc, lỗi nếu không tồn tại
open("file.txt", "w")    # Write — ghi mới, xóa nội dung cũ nếu tồn tại
open("file.txt", "a")    # Append — ghi thêm vào cuối
open("file.txt", "x")    # Exclusive create — tạo mới, lỗi nếu đã tồn tại
open("file.txt", "r+")   # Read + Write — đọc và ghi, không xóa nội dung

# Chế độ binary — thêm "b"
open("image.png", "rb")  # Đọc binary
open("image.png", "wb")  # Ghi binary

# Luôn chỉ định encoding khi làm việc với text
open("file.txt", "r", encoding="utf-8")
```

| Chế độ | Đọc | Ghi | Tạo mới | Xóa nội dung cũ |
|--------|-----|-----|---------|-----------------|
| `r`    | ✅  | ❌  | ❌      | ❌              |
| `w`    | ❌  | ✅  | ✅      | ✅              |
| `a`    | ❌  | ✅  | ✅      | ❌              |
| `x`    | ❌  | ✅  | ✅ (lỗi nếu tồn tại) | ❌ |
| `r+`   | ✅  | ✅  | ❌      | ❌              |

### 1.3 Các Phương Thức Đọc

```python
# Tạo file mẫu để thử nghiệm
with open("sample.txt", "w", encoding="utf-8") as f:
    f.write("Dòng 1: Hello World\n")
    f.write("Dòng 2: Python is great\n")
    f.write("Dòng 3: FastAPI rocks\n")

# read() — đọc toàn bộ thành một string
with open("sample.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(repr(content))
    # 'Dòng 1: Hello World\nDòng 2: Python is great\nDòng 3: FastAPI rocks\n'

# read(n) — đọc n ký tự
with open("sample.txt", "r", encoding="utf-8") as f:
    chunk = f.read(10)
    print(chunk)    # Dòng 1: He

# readline() — đọc một dòng
with open("sample.txt", "r", encoding="utf-8") as f:
    line1 = f.readline()    # "Dòng 1: Hello World\n"
    line2 = f.readline()    # "Dòng 2: Python is great\n"
    print(line1.strip())    # Bỏ \n cuối

# readlines() — đọc tất cả dòng vào list
with open("sample.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()   # ['Dòng 1: Hello World\n', ...]
    for line in lines:
        print(line.strip())

# Duyệt file object trực tiếp — TỐT NHẤT cho file lớn (lazy, không load vào RAM)
with open("sample.txt", "r", encoding="utf-8") as f:
    for line in f:          # File object là iterable
        print(line.strip())
```

### 1.4 Con Trỏ File — `seek()` và `tell()`

```python
with open("sample.txt", "r", encoding="utf-8") as f:
    print(f.tell())     # 0 — vị trí hiện tại (bytes từ đầu)

    f.read(10)
    print(f.tell())     # 10

    f.seek(0)           # Quay về đầu file
    print(f.read(5))    # Dòng
    
    f.seek(0, 2)        # Nhảy đến cuối file (whence=2)
    print(f.tell())     # Kích thước file (bytes)
```

---

## 2. Ghi File và Tối Ưu Hóa Bằng Buffer

### 2.1 Ghi File Cơ Bản

```python
# write() — ghi string, trả về số ký tự đã ghi
with open("output.txt", "w", encoding="utf-8") as f:
    n = f.write("Hello, World!\n")  # n = 14
    f.write("Dòng thứ hai\n")

# writelines() — ghi list các string (không tự thêm \n)
lines = ["Dòng 1\n", "Dòng 2\n", "Dòng 3\n"]
with open("output.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)

# Append — ghi thêm vào cuối, không xóa nội dung cũ
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("[2026-05-22 10:00:00] Server started\n")
```

### 2.2 Tối Ưu Bằng Buffer

> **Java tương đương:** `BufferedWriter` bọc ngoài `FileWriter` để giảm số lần I/O. Python `open()` đã tự buffer theo mặc định.

```python
import io

# buffering=0   → tắt buffer (chỉ dùng mode binary)
# buffering=1   → line buffer (chỉ dùng mode text)
# buffering=N   → buffer size N bytes
# buffering=-1  → mặc định (thường 8192 bytes)

# Mặc định — Python đã dùng buffer 8192 bytes (hiệu quả cho hầu hết trường hợp)
with open("output.txt", "w", encoding="utf-8") as f:
    for i in range(10000):
        f.write(f"Record {i}\n")    # Dữ liệu được gom trong buffer, flush khi đầy

# flush() — ghi buffer ra disk ngay lập tức (dùng khi cần đảm bảo dữ liệu được lưu)
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("Critical error!\n")
    f.flush()   # Đảm bảo ghi ra disk ngay — quan trọng với log

# StringIO — file ảo trong memory (Java: StringWriter)
buffer = io.StringIO()
buffer.write("Hello ")
buffer.write("World")
result = buffer.getvalue()  # "Hello World"
buffer.close()

# Ứng dụng: build string lớn hiệu quả hơn += (tương tự StringBuilder Java)
import io
parts = io.StringIO()
for i in range(1000):
    parts.write(f"Item {i}, ")
text = parts.getvalue()
```

### 2.3 Ghi File Binary

```python
# Sao chép file ảnh
with open("source.jpg", "rb") as src:
    with open("copy.jpg", "wb") as dst:
        while chunk := src.read(8192):  # Walrus operator — đọc từng chunk 8KB
            dst.write(chunk)

# Cách ngắn hơn với shutil
import shutil
shutil.copy("source.jpg", "copy.jpg")          # Copy file
shutil.copy2("source.jpg", "backup/copy.jpg")  # Copy + giữ metadata
```

---

## 3. Đọc và Ghi File JSON, CSV

### 3.1 JSON

> **Java tương đương:** `ObjectMapper` của Jackson. Python có module `json` trong standard library — không cần thư viện ngoài.

```python
import json

# Dữ liệu Python → JSON string
data = {
    "name": "Hoàng",
    "age": 28,
    "skills": ["Python", "FastAPI", "Java"],
    "active": True,
    "score": None   # None → null trong JSON
}

# json.dumps() — serialize thành string
json_str = json.dumps(data)
print(json_str)
# {"name": "Hoàng", "age": 28, "skills": ["Python", "FastAPI", "Java"], ...}

# ensure_ascii=False — giữ nguyên ký tự Unicode
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)
# {
#   "name": "Hoàng",
#   "age": 28, ...
# }

# json.loads() — parse từ string
parsed = json.loads(json_str)
print(type(parsed))     # <class 'dict'>
print(parsed["name"])   # Hoàng
```

```python
import json

# Ghi JSON ra file
employees = [
    {"id": 1, "name": "Alice", "dept": "Engineering", "salary": 35_000_000},
    {"id": 2, "name": "Bob",   "dept": "Marketing",   "salary": 28_000_000},
]

with open("employees.json", "w", encoding="utf-8") as f:
    json.dump(employees, f, ensure_ascii=False, indent=2)

# Đọc JSON từ file
with open("employees.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)

print(loaded[0]["name"])    # Alice
print(type(loaded))         # <class 'list'>
```

```python
import json
from datetime import datetime

# Custom serializer — xử lý kiểu Python mà JSON không hỗ trợ
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # datetime → "2026-05-22T10:00:00"
        if isinstance(obj, set):
            return list(obj)        # set → list
        return super().default(obj)

record = {
    "event": "login",
    "timestamp": datetime(2026, 5, 22, 10, 0, 0),
    "tags": {"admin", "vip"}
}

json_str = json.dumps(record, cls=CustomEncoder, ensure_ascii=False)
print(json_str)
# {"event": "login", "timestamp": "2026-05-22T10:00:00", "tags": ["admin", "vip"]}
```

### 3.2 CSV

> **Java tương đương:** Apache Commons CSV hoặc OpenCSV. Python có module `csv` trong standard library.

```python
import csv

# Ghi CSV
employees = [
    ["id", "name", "department", "salary"],         # Header
    [1, "Alice", "Engineering", 35_000_000],
    [2, "Bob",   "Marketing",   28_000_000],
    [3, "Charlie","Engineering", 40_000_000],
]

with open("employees.csv", "w", newline="", encoding="utf-8") as f:
    # newline="" — quan trọng trên Windows để tránh dòng trống thêm
    writer = csv.writer(f)
    writer.writerows(employees)

# Đọc CSV
with open("employees.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)           # Đọc dòng đầu tiên làm header
    print(f"Columns: {header}")

    for row in reader:
        print(f"  {row[1]} ({row[2]}): {int(row[3]):,} VND")
```

```python
import csv

# DictReader / DictWriter — đọc ghi theo tên cột (tiện hơn)
data = [
    {"name": "Alice",   "dept": "Engineering", "salary": 35_000_000},
    {"name": "Bob",     "dept": "Marketing",   "salary": 28_000_000},
    {"name": "Charlie", "dept": "Engineering", "salary": 40_000_000},
]

# DictWriter — ghi dict
fieldnames = ["name", "dept", "salary"]
with open("staff.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()        # Ghi dòng header
    writer.writerows(data)

# DictReader — đọc thành dict (tiện hơn reader thường)
with open("staff.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['name']:10} | {row['dept']:15} | {int(row['salary']):>12,}")
# Alice      | Engineering     |   35,000,000
# Bob        | Marketing       |   28,000,000
```

---

## 4. Giới Thiệu Module — `import`, `from...import`, Alias

### 4.1 Cú Pháp Import

> **Java tương đương:** `import com.example.MyClass;` — nhưng Python import linh hoạt hơn nhiều.

```python
# Import toàn bộ module
import math
import os
import datetime

print(math.pi)          # 3.141592653589793
print(math.sqrt(16))    # 4.0
print(os.getcwd())      # Thư mục hiện tại

# from...import — import cụ thể từ module
from math import pi, sqrt, ceil
from os import getcwd, listdir
from datetime import datetime, timedelta

print(pi)               # 3.141592653589793 — không cần math.pi
print(sqrt(25))         # 5.0

# Alias — đổi tên khi import
import numpy as np          # Convention phổ biến
import pandas as pd         # Convention phổ biến
from datetime import datetime as dt

now = dt.now()
print(now)

# from module import * — KHÔNG khuyến khích (gây ô nhiễm namespace)
# from math import *    # Tránh dùng trong code production
```

### 4.2 Thứ Tự Tìm Kiếm Module

```python
import sys

# Python tìm module theo thứ tự:
# 1. sys.modules (cache — đã import trước đó)
# 2. Built-in modules (math, os, sys...)
# 3. Các đường dẫn trong sys.path (gồm thư mục hiện tại, site-packages...)

print(sys.path)     # Danh sách các thư mục Python tìm module

# Kiểm tra module đã được cache
import math
print("math" in sys.modules)    # True — đã import
```

### 4.3 `if __name__ == "__main__"`

> **Java tương đương:** `public static void main(String[] args)` — điểm vào chương trình. Python dùng convention `if __name__ == "__main__"` để phân biệt chạy trực tiếp vs bị import.

```python
# utils.py
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

# Code này chỉ chạy khi file được chạy trực tiếp
# Không chạy khi bị import từ module khác
if __name__ == "__main__":
    print("Chạy trực tiếp utils.py")
    print(add(3, 5))        # 8
    print(multiply(4, 6))   # 24

# main.py
# import utils
# print(utils.add(10, 20))  # 30 — không in "Chạy trực tiếp..."
```

---

## 5. Các Module Có Sẵn Quan Trọng

### 5.1 `os` và `sys`

```python
import os
import sys

# os — tương tác với hệ điều hành
print(os.getcwd())                  # Thư mục hiện tại
os.chdir("/tmp")                    # Đổi thư mục

print(os.listdir("."))              # Danh sách file/thư mục
print(os.path.exists("file.txt"))   # Kiểm tra tồn tại
print(os.path.isfile("file.txt"))   # Là file?
print(os.path.isdir("/tmp"))        # Là thư mục?

os.makedirs("a/b/c", exist_ok=True) # Tạo thư mục lồng nhau (như mkdir -p)
os.remove("file.txt")               # Xóa file
os.rename("old.txt", "new.txt")     # Đổi tên

# os.path — xử lý đường dẫn
path = os.path.join("users", "hoang", "file.txt")  # users/hoang/file.txt
print(os.path.dirname(path))        # users/hoang
print(os.path.basename(path))       # file.txt
print(os.path.splitext("file.txt")) # ('file', '.txt')
print(os.path.abspath("file.txt"))  # Đường dẫn tuyệt đối

# Biến môi trường
print(os.environ.get("HOME", "/root"))  # Đọc env var với default
os.environ["MY_VAR"] = "hello"          # Đặt env var

# sys — thông tin Python runtime
print(sys.version)          # Phiên bản Python
print(sys.platform)         # 'win32', 'linux', 'darwin'
print(sys.argv)             # Tham số dòng lệnh
sys.exit(0)                 # Thoát chương trình (giống System.exit(0))
```

### 5.2 `pathlib` — Modern Path Handling

> `pathlib` là cách hiện đại hơn `os.path` — dùng OOP thay vì hàm. Python 3.4+.

```python
from pathlib import Path

# Tạo Path object
p = Path("users/hoang/data")
home = Path.home()          # Thư mục home của user
cwd  = Path.cwd()           # Thư mục hiện tại

# Nối đường dẫn bằng / (operator overloading)
config_file = home / ".config" / "app" / "settings.json"
print(config_file)          # C:\Users\hoang\.config\app\settings.json (Windows)

# Thông tin file
print(config_file.name)     # settings.json
print(config_file.stem)     # settings
print(config_file.suffix)   # .json
print(config_file.parent)   # C:\Users\hoang\.config\app

# Kiểm tra
print(config_file.exists())     # True/False
print(config_file.is_file())    # True/False
print(config_file.is_dir())     # True/False

# Tạo thư mục
output_dir = Path("output/reports")
output_dir.mkdir(parents=True, exist_ok=True)   # Tương đương os.makedirs

# Đọc/ghi file ngắn gọn
p = Path("data.txt")
p.write_text("Hello, World!", encoding="utf-8")         # Ghi
content = p.read_text(encoding="utf-8")                  # Đọc

p.write_bytes(b"\x89PNG\r\n\x1a\n")    # Ghi binary
data = p.read_bytes()                   # Đọc binary

# Liệt kê file
src = Path("src")
for py_file in src.rglob("*.py"):       # Tìm đệ quy — rglob
    print(py_file)

for item in Path(".").iterdir():        # Liệt kê thư mục hiện tại
    if item.is_file():
        print(f"  FILE: {item.name} ({item.stat().st_size} bytes)")
```

### 5.3 `datetime`

```python
from datetime import datetime, date, time, timedelta
import datetime as dt_module

# Tạo datetime
now = datetime.now()            # Thời điểm hiện tại (local)
today = date.today()            # Ngày hôm nay
specific = datetime(2026, 5, 22, 10, 30, 0)

print(now)          # 2026-05-22 10:30:00.123456
print(today)        # 2026-05-22

# Các thuộc tính
print(now.year, now.month, now.day)         # 2026 5 22
print(now.hour, now.minute, now.second)     # 10 30 0
print(now.weekday())    # 3 (thứ Năm — 0=Monday)

# Format và parse — Java: DateTimeFormatter
# strftime — datetime → string
print(now.strftime("%Y-%m-%d"))             # 2026-05-22
print(now.strftime("%d/%m/%Y %H:%M:%S"))   # 22/05/2026 10:30:00
print(now.strftime("%A, %B %d, %Y"))       # Thursday, May 22, 2026

# strptime — string → datetime
d = datetime.strptime("22/05/2026", "%d/%m/%Y")
print(type(d))      # <class 'datetime.datetime'>

# Phép tính với timedelta
tomorrow   = today + timedelta(days=1)
last_week  = today - timedelta(weeks=1)
in_2_hours = now + timedelta(hours=2)

diff = datetime(2026, 12, 31) - now
print(f"Còn {diff.days} ngày đến cuối năm")

# ISO format — tiêu chuẩn cho API
print(now.isoformat())              # 2026-05-22T10:30:00.123456
back = datetime.fromisoformat("2026-05-22T10:30:00")
```

### 5.4 `json` và `re`

```python
import json

# json — đã học ở phần 3, ôn lại nhanh các tip
data = '{"name": "Hoàng", "scores": [85, 92, 78]}'
obj = json.loads(data)
print(obj["scores"][0])     # 85

# sort_keys — sắp xếp key khi dump (tiện cho so sánh/debug)
print(json.dumps(obj, sort_keys=True, ensure_ascii=False))
```

```python
import re

# re — Regular Expression (Java: java.util.regex)
text = "Email: hoang@digidinos.com và support@example.com lúc 10:30"

# re.findall() — tìm tất cả kết quả khớp
emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text)
print(emails)   # ['hoang@digidinos.com', 'support@example.com']

# re.search() — tìm kết quả đầu tiên
match = re.search(r"\d{1,2}:\d{2}", text)
if match:
    print(match.group())    # 10:30
    print(match.start())    # Vị trí bắt đầu

# re.match() — chỉ khớp từ đầu string
m = re.match(r"Email:", text)
print(bool(m))  # True

# re.sub() — thay thế (Java: String.replaceAll với regex)
cleaned = re.sub(r"\s+", " ", "  quá   nhiều   khoảng   trắng  ")
print(cleaned)  # " quá nhiều khoảng trắng "

# re.split() — tách chuỗi theo regex
parts = re.split(r"[,;\s]+", "Alice, Bob; Charlie  Dave")
print(parts)    # ['Alice', 'Bob', 'Charlie', 'Dave']

# Compile pattern nếu dùng nhiều lần (hiệu quả hơn)
email_pattern = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
emails2 = email_pattern.findall("another@test.com và more@mail.org")

# Named groups — trích xuất có tên
date_pattern = re.compile(r"(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})")
m = date_pattern.search("Ngày sinh: 15/03/1995")
if m:
    print(m.group("day"), m.group("month"), m.group("year"))  # 15 03 1995
```

---

## 6. Tự Xây Dựng Package và Module

### 6.1 Module

```python
# Một file .py = một module

# calculator.py
"""Module cung cấp các phép tính cơ bản."""

PI = 3.14159265358979

def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Không thể chia cho 0")
    return a / b

# main.py (cùng thư mục)
import calculator

print(calculator.PI)
print(calculator.add(3, 5))         # 8
print(calculator.divide(10, 3))     # 3.333...

from calculator import add, multiply
print(add(10, 20))      # 30
```

### 6.2 Package

```python
# Package = thư mục có file __init__.py
#
# myapp/
# ├── __init__.py          ← Đánh dấu đây là package
# ├── models/
# │   ├── __init__.py
# │   ├── user.py
# │   └── product.py
# ├── services/
# │   ├── __init__.py
# │   ├── auth.py
# │   └── payment.py
# └── utils/
#     ├── __init__.py
#     └── helpers.py

# myapp/models/user.py
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"User(name={self.name!r}, email={self.email!r})"

# myapp/models/__init__.py — kiểm soát API công khai của package
from .user import User
from .product import Product

# myapp/__init__.py
from .models import User, Product
from .services.auth import authenticate

# Import từ package
from myapp.models.user import User          # Import tường minh
from myapp.models import User, Product      # Qua __init__.py của models
from myapp import User                      # Qua __init__.py của myapp (nếu re-export)
```

### 6.3 `__init__.py` và Relative Import

```python
# myapp/services/auth.py
from myapp.models.user import User      # Absolute import
from ..models.user import User          # Relative import (.. = lên một cấp)
from .payment import process_payment    # Relative import (. = cùng cấp)

# __init__.py — kiểm soát những gì export ra ngoài
# myapp/models/__init__.py
from .user import User
from .product import Product

__all__ = ["User", "Product"]   # Kiểm soát 'from myapp.models import *'
```

---

## 7. Exception Handling P1 — `try` / `except` / `finally`

### 7.1 Cú Pháp Cơ Bản

> **Java developer:** Gần giống Java, nhưng `except` thay vì `catch`, và Python không có checked exception.

```python
# Java:
# try {
#     int result = 10 / 0;
# } catch (ArithmeticException e) {
#     System.out.println("Lỗi: " + e.getMessage());
# } finally {
#     System.out.println("Luôn chạy");
# }

# Python:
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Lỗi: {e}")     # Lỗi: division by zero
finally:
    print("Luôn chạy")      # Dù có exception hay không

# Bắt nhiều loại exception
def parse_config(filename: str) -> dict:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            import json
            return json.load(f)
    except FileNotFoundError:
        print(f"Không tìm thấy file: {filename}")
        return {}
    except json.JSONDecodeError as e:
        print(f"File JSON không hợp lệ: {e}")
        return {}
    except PermissionError:
        print(f"Không có quyền đọc: {filename}")
        return {}
```

### 7.2 `else` Clause — Chỉ Chạy Khi Không Có Exception

> **Java không có** `else` trong try-catch. Đây là tính năng riêng của Python.

```python
def read_number(prompt: str) -> int | None:
    try:
        value = int(input(prompt))
    except ValueError:
        print("Nhập số nguyên hợp lệ!")
        return None
    else:
        # Chỉ chạy khi try thành công — không có exception
        print(f"Bạn nhập: {value}")
        return value
    finally:
        # Luôn chạy — dù có exception hay không, dù có return trong try/except
        print("Kết thúc hàm read_number")
```

```python
# Thứ tự thực thi — quan trọng để hiểu đúng
def demo():
    try:
        print("1. try")
        # raise ValueError("test")   # Thử bỏ comment dòng này
        print("2. try (sau raise nếu có)")
    except ValueError:
        print("3. except (chỉ khi có ValueError)")
    else:
        print("4. else (chỉ khi try thành công)")
    finally:
        print("5. finally (LUÔN chạy)")

demo()
# Không có exception:    1 → 2 → 4 → 5
# Có exception:          1 → 3 → 5
```

### 7.3 Hierarchy Exception và `Exception` Base Class

```python
# Python exception hierarchy (một số quan trọng):
# BaseException
#   ├── SystemExit                ← sys.exit()
#   ├── KeyboardInterrupt         ← Ctrl+C
#   └── Exception
#       ├── ValueError            ← Giá trị không hợp lệ
#       ├── TypeError             ← Kiểu dữ liệu sai
#       ├── AttributeError        ← Attribute không tồn tại
#       ├── IndexError            ← Index ngoài phạm vi
#       ├── KeyError              ← Key không tồn tại trong dict
#       ├── FileNotFoundError     ← (con của OSError)
#       ├── PermissionError       ← (con của OSError)
#       ├── ZeroDivisionError     ← (con của ArithmeticError)
#       └── ImportError           ← Import thất bại

# Bắt nhiều exception một lúc — tuple
try:
    data = int("abc")
except (ValueError, TypeError) as e:
    print(f"Lỗi chuyển đổi: {e}")

# Bắt tất cả exception (KHÔNG khuyến khích — che giấu lỗi)
try:
    risky_operation()
except Exception as e:
    print(f"Lỗi không mong đợi: {type(e).__name__}: {e}")
    raise   # Re-raise để không nuốt exception

# KHÔNG BAO GIỜ catch BaseException trừ khi bạn biết mình làm gì
# except BaseException:  # Bắt cả KeyboardInterrupt, SystemExit — nguy hiểm
```

### 7.4 `raise` và Re-raise

```python
def withdraw(balance: float, amount: float) -> float:
    if amount <= 0:
        raise ValueError(f"Số tiền phải dương, nhận: {amount}")
    if amount > balance:
        raise ValueError(f"Không đủ tiền. Số dư: {balance:,}, cần: {amount:,}")
    return balance - amount

# Re-raise — log rồi throw lại
def process_payment(amount: float) -> bool:
    try:
        new_balance = withdraw(current_balance, amount)
        return True
    except ValueError as e:
        print(f"[LOG] Payment failed: {e}")
        raise   # Throw lại exception gốc — không nuốt

# Exception chaining — Python 3
def load_config(path: str) -> dict:
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise RuntimeError(f"Config file không tìm thấy: {path}") from e
        # Giữ context — "The above exception was the direct cause of..."
```

### 7.5 Context Manager và Exception

```python
# with statement dùng __enter__ và __exit__ — xử lý exception tự động
class ManagedResource:
    def __enter__(self):
        print("Mở resource")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Đóng resource (exc_type={exc_type})")
        # Trả về True → suppress exception (không raise tiếp)
        # Trả về False/None → exception tiếp tục propagate
        return False

with ManagedResource() as r:
    print("Dùng resource")
    # raise ValueError("test")  # __exit__ vẫn được gọi

# contextlib.contextmanager — tạo context manager từ generator
from contextlib import contextmanager

@contextmanager
def timer(label: str):
    import time
    start = time.perf_counter()
    try:
        yield   # Code trong with block chạy ở đây
    finally:
        elapsed = time.perf_counter() - start
        print(f"[{label}] {elapsed:.4f}s")

with timer("database query"):
    # Simulate slow query
    import time; time.sleep(0.1)
# [database query] 0.1002s
```

---

## 8. Exception Handling P2 — Custom Exception

### 8.1 Xây Dựng Custom Exception

> **Java tương đương:** Extend `RuntimeException` hoặc `Exception`. Python cũng extend từ `Exception`.

```python
# Base exception cho toàn bộ ứng dụng
class AppError(Exception):
    """Base exception cho ứng dụng."""
    pass

# Domain-specific exceptions
class ValidationError(AppError):
    """Dữ liệu đầu vào không hợp lệ."""

    def __init__(self, field: str, message: str, value=None):
        self.field = field
        self.value = value
        super().__init__(f"Validation failed — {field}: {message}")

class NotFoundError(AppError):
    """Resource không tồn tại."""

    def __init__(self, resource: str, identifier):
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} không tìm thấy với id={identifier}")

class PermissionDeniedError(AppError):
    """Không có quyền thực hiện hành động."""

    def __init__(self, action: str, user: str):
        self.action = action
        self.user = user
        super().__init__(f"User '{user}' không có quyền '{action}'")

# Sử dụng
try:
    raise ValidationError("email", "Định dạng không hợp lệ", value="not-an-email")
except ValidationError as e:
    print(e)            # Validation failed — email: Định dạng không hợp lệ
    print(e.field)      # email
    print(e.value)      # not-an-email

try:
    raise NotFoundError("User", 999)
except NotFoundError as e:
    print(e)            # User không tìm thấy với id=999
    print(e.resource)   # User
```

### 8.2 Exception Hierarchy Cho Domain

```python
# Thiết kế exception hierarchy cho hệ thống thương mại điện tử
class EcommerceError(Exception):
    """Root exception — bắt tất cả lỗi của domain này."""
    pass

class ProductError(EcommerceError):
    pass

class OrderError(EcommerceError):
    pass

class PaymentError(EcommerceError):
    pass

# ProductError subtypes
class ProductNotFoundError(ProductError):
    def __init__(self, product_id: int):
        super().__init__(f"Sản phẩm #{product_id} không tồn tại")
        self.product_id = product_id

class OutOfStockError(ProductError):
    def __init__(self, product_id: int, requested: int, available: int):
        super().__init__(
            f"Sản phẩm #{product_id} không đủ hàng "
            f"(yêu cầu: {requested}, còn: {available})"
        )
        self.product_id = product_id
        self.requested = requested
        self.available = available

# PaymentError subtypes
class InsufficientFundsError(PaymentError):
    def __init__(self, required: float, available: float):
        super().__init__(
            f"Không đủ tiền: cần {required:,.0f} VND, có {available:,.0f} VND"
        )
        self.shortfall = required - available

class PaymentGatewayError(PaymentError):
    def __init__(self, gateway: str, reason: str):
        super().__init__(f"[{gateway}] Thanh toán thất bại: {reason}")
        self.gateway = gateway

# Service sử dụng
def place_order(product_id: int, quantity: int, user_balance: float) -> dict:
    # Giả lập data
    products = {1: {"name": "Laptop", "price": 25_000_000, "stock": 2}}

    if product_id not in products:
        raise ProductNotFoundError(product_id)

    product = products[product_id]

    if product["stock"] < quantity:
        raise OutOfStockError(product_id, quantity, product["stock"])

    total = product["price"] * quantity
    if user_balance < total:
        raise InsufficientFundsError(total, user_balance)

    return {"product": product["name"], "quantity": quantity, "total": total}

# Client code — bắt theo mức độ cụ thể cần thiết
def process_order(product_id: int, quantity: int, balance: float):
    try:
        order = place_order(product_id, quantity, balance)
        print(f"Đặt hàng thành công: {order}")

    except OutOfStockError as e:
        print(f"Hết hàng: {e} | Thiếu: {e.requested - e.available} sản phẩm")

    except InsufficientFundsError as e:
        print(f"Không đủ tiền: {e} | Cần thêm: {e.shortfall:,.0f} VND")

    except ProductError as e:
        # Bắt mọi ProductError — kể cả ProductNotFoundError
        print(f"Lỗi sản phẩm: {e}")

    except EcommerceError as e:
        # Bắt tất cả lỗi domain — fallback
        print(f"Lỗi hệ thống: {e}")

process_order(1, 5, 100_000_000)    # OutOfStockError
process_order(1, 1, 10_000_000)     # InsufficientFundsError
process_order(99, 1, 100_000_000)   # ProductNotFoundError
```

### 8.3 Best Practices

```python
from contextlib import suppress

# 1. Dùng suppress() cho exception muốn bỏ qua — gọn hơn try/except/pass
with suppress(FileNotFoundError):
    import os; os.remove("temp.txt")  # Bỏ qua nếu file không tồn tại

# 2. EAFP vs LBYL — Python ưu tiên EAFP
# LBYL (Look Before You Leap) — Java style
if "key" in my_dict:
    value = my_dict["key"]

# EAFP (Easier to Ask Forgiveness than Permission) — Python style
try:
    value = my_dict["key"]
except KeyError:
    value = default_value

# Hoặc dùng .get() — Pythonic nhất
value = my_dict.get("key", default_value)

# 3. Không nuốt exception im lặng
# BAD
try:
    risky()
except Exception:
    pass    # Nuốt hoàn toàn — khó debug

# GOOD
try:
    risky()
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise   # Hoặc xử lý đúng cách

# 4. Exception message rõ ràng
# BAD
raise ValueError("Invalid")

# GOOD
raise ValueError(
    f"Giá trị không hợp lệ: expected positive int, got {value!r} ({type(value).__name__})"
)
```

---

## Tóm Tắt — So Sánh Nhanh Java vs Python

| Khái niệm               | Java                                   | Python                                      |
|-------------------------|----------------------------------------|---------------------------------------------|
| Mở file                 | `new FileReader(path)` + try-finally   | `with open(path, mode, encoding=...) as f:` |
| Auto-close              | `try-with-resources`                   | `with` statement                            |
| Đọc toàn bộ             | `Files.readString(Path)`              | `f.read()` hoặc `Path.read_text()`         |
| Đọc từng dòng           | `br.readLine()` / `Files.lines()`      | `for line in f:` (lazy iterator)           |
| JSON                    | Jackson `ObjectMapper`                 | `import json` (standard library)           |
| CSV                     | Apache Commons CSV                     | `import csv` (standard library)            |
| Path handling           | `java.nio.file.Path`, `Paths.get()`   | `pathlib.Path` / `os.path`                 |
| Import                  | `import com.example.Class;`           | `import module` / `from mod import Class`  |
| Package                 | Directory + `package` statement        | Directory + `__init__.py`                  |
| try-catch-finally       | `try { } catch (E e) { } finally { }` | `try: except E: else: finally:`            |
| Checked exception       | Bắt buộc khai báo trong method sig     | Không có — mọi exception đều unchecked     |
| Custom exception        | `class MyEx extends RuntimeException` | `class MyEx(Exception):`                   |
| Re-raise                | `throw;` (không tham số)              | `raise` (không tham số)                    |
| Exception chaining      | `throw new Ex("msg", cause)`          | `raise Ex("msg") from cause`               |
| Suppress exception      | try-catch với empty body               | `with contextlib.suppress(ExType):`        |
| `else` trong try        | Không có                               | `else:` — chỉ chạy khi không có exception  |

---

## Bài Tập Thực Hành

Tạo file `practice_07.py` và viết code cho các bài sau:

```python
# ============================================================
# PHẦN 1 — File I/O
# ============================================================

# Bài 1: Đọc file CSV, xử lý dữ liệu, ghi file JSON
# - Đọc file employees.csv (tạo trong bài nếu chưa có)
# - Tính lương trung bình theo phòng ban
# - Ghi kết quả ra report.json

import csv
import json
from pathlib import Path
from collections import defaultdict

# Tạo file mẫu
Path("employees.csv").write_text(
    "name,department,salary\n"
    "Alice,Engineering,35000000\n"
    "Bob,Marketing,28000000\n"
    "Charlie,Engineering,40000000\n"
    "Dave,Marketing,32000000\n"
    "Eve,Engineering,38000000\n",
    encoding="utf-8"
)

# Đọc và xử lý
dept_salaries: dict[str, list[int]] = defaultdict(list)

with open("employees.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        dept_salaries[row["department"]].append(int(row["salary"]))

report = {
    dept: {
        "count": len(salaries),
        "avg_salary": sum(salaries) / len(salaries),
        "total_budget": sum(salaries)
    }
    for dept, salaries in dept_salaries.items()
}

with open("report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("Report đã ghi vào report.json")
with open("report.json", "r", encoding="utf-8") as f:
    print(f.read())


# Bài 2: Log writer với rotation
# - Ghi log vào file, mỗi dòng có timestamp
# - Nếu file > 1KB thì rotate sang file mới (backup)
from datetime import datetime
import os

class SimpleLogger:
    def __init__(self, path: str, max_bytes: int = 1024):
        self.path = Path(path)
        self.max_bytes = max_bytes

    def _rotate(self) -> None:
        backup = self.path.with_suffix(".log.bak")
        if backup.exists():
            backup.unlink()
        self.path.rename(backup)

    def log(self, level: str, message: str) -> None:
        if self.path.exists() and self.path.stat().st_size > self.max_bytes:
            self._rotate()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{level}] {message}\n")
            f.flush()

logger = SimpleLogger("app.log", max_bytes=200)
for i in range(10):
    logger.log("INFO", f"Processing record #{i}")
logger.log("ERROR", "Something went wrong")

print(f"app.log size: {Path('app.log').stat().st_size} bytes")
if Path("app.log.bak").exists():
    print("Rotated! app.log.bak tồn tại")


# ============================================================
# PHẦN 2 — Module, pathlib, regex
# ============================================================

# Bài 3: Dùng pathlib tìm file trong thư mục
from pathlib import Path
import re

def find_files(root: str, pattern: str, min_size_bytes: int = 0) -> list[dict]:
    """Tìm file theo pattern regex trong cây thư mục."""
    results = []
    for p in Path(root).rglob("*"):
        if p.is_file() and re.search(pattern, p.name):
            stat = p.stat()
            if stat.st_size >= min_size_bytes:
                results.append({
                    "path": str(p),
                    "name": p.name,
                    "size": stat.st_size,
                    "ext": p.suffix,
                })
    return sorted(results, key=lambda f: f["size"], reverse=True)

# Tìm tất cả file .py trong thư mục hiện tại
py_files = find_files(".", r"\.py$")
for f in py_files[:5]:
    print(f"{f['name']:30} {f['size']:>8} bytes")


# ============================================================
# PHẦN 3 — Exception Handling
# ============================================================

# Bài 4: Xây dựng hệ thống xử lý lỗi cho config loader
import json
from pathlib import Path

class ConfigError(Exception):
    pass

class ConfigNotFoundError(ConfigError):
    def __init__(self, path: str):
        super().__init__(f"Config file không tìm thấy: {path}")
        self.path = path

class ConfigParseError(ConfigError):
    def __init__(self, path: str, detail: str):
        super().__init__(f"Config file không hợp lệ [{path}]: {detail}")
        self.path = path

class ConfigValidationError(ConfigError):
    def __init__(self, field: str, reason: str):
        super().__init__(f"Config validation failed — {field}: {reason}")
        self.field = field

def load_config(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        raise ConfigNotFoundError(path)
    except json.JSONDecodeError as e:
        raise ConfigParseError(path, str(e)) from e

    # Validate
    required = ["host", "port", "database"]
    for field in required:
        if field not in config:
            raise ConfigValidationError(field, "Trường bắt buộc bị thiếu")

    if not isinstance(config["port"], int) or not (1 <= config["port"] <= 65535):
        raise ConfigValidationError("port", f"Phải là int từ 1-65535, nhận: {config['port']!r}")

    return config

# Test
test_cases = [
    ("nonexistent.json", "File không tồn tại"),
    ("bad_config.json", "JSON không hợp lệ"),
    ("missing_field.json", "Thiếu trường bắt buộc"),
    ("valid_config.json", "Config hợp lệ"),
]

# Tạo file test
Path("bad_config.json").write_text("{ not valid json", encoding="utf-8")
Path("missing_field.json").write_text('{"host": "localhost"}', encoding="utf-8")
Path("valid_config.json").write_text(
    '{"host": "localhost", "port": 5432, "database": "myapp"}',
    encoding="utf-8"
)

for filename, description in test_cases:
    print(f"\n--- {description} ---")
    try:
        config = load_config(filename)
        print(f"OK: {config}")
    except ConfigNotFoundError as e:
        print(f"ConfigNotFoundError: {e}")
    except ConfigParseError as e:
        print(f"ConfigParseError: {e}")
    except ConfigValidationError as e:
        print(f"ConfigValidationError: {e} (field={e.field})")
    except ConfigError as e:
        print(f"ConfigError: {e}")
```
