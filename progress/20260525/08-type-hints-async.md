# 08 — Type Hints & Async Programming

> **Khối 7 — Type Hints & Async Programming**
> Dành cho Java developer — tập trung vào điểm khác biệt so với Java.

---

## 1. Giới Thiệu Type Hints — `int`, `str`, `list`, `dict`, `Optional`

### 1.1 Tại Sao Cần Type Hints?

> **Java developer:** Java có kiểu tĩnh bắt buộc — trình biên dịch bắt lỗi kiểu tại compile time. Python là kiểu động — type hints chỉ là **gợi ý tùy chọn**, không được enforce ở runtime. Tuy nhiên, chúng giúp IDE, mypy, và FastAPI hiểu code hơn.

```python
# Không có type hints — Python hoàn toàn hợp lệ, nhưng khó đọc
def process(data, limit):
    result = []
    for item in data:
        if item > limit:
            result.append(item)
    return result

# Có type hints — rõ ràng hơn, IDE autocomplete tốt hơn
def process(data: list[int], limit: int) -> list[int]:
    result: list[int] = []
    for item in data:
        if item > limit:
            result.append(item)
    return result

# Type hints không enforce tại runtime — Python không báo lỗi dòng dưới
x: int = "hello"   # Không lỗi runtime! Nhưng mypy sẽ báo lỗi
```

```python
# Dùng reveal_type() để kiểm tra kiểu (chỉ dùng với mypy, không chạy runtime)
# $ mypy script.py

# Kiểu cơ bản — Python 3.12+
name: str = "Hoàng"
age: int = 28
height: float = 1.75
is_active: bool = True
data: bytes = b"\x00\x01"

# Khai báo biến chưa gán — dùng khi cần khai báo trước
user_id: int          # Chỉ khai báo, chưa gán giá trị
user_id = 42          # Gán sau

# Kiểm tra kiểu tại runtime (hiếm dùng, chỉ khi thực sự cần)
def greet(name: str) -> str:
    if not isinstance(name, str):     # Validate thủ công nếu muốn
        raise TypeError(f"Cần str, nhận {type(name).__name__}")
    return f"Xin chào, {name}!"
```

### 1.2 Collection Types — Python 3.9+

> **Python 3.9+:** Dùng trực tiếp `list[int]`, `dict[str, int]` thay vì `List[int]`, `Dict[str, int]` từ `typing`. Python 3.12+ tiếp tục hỗ trợ cả hai.

```python
# Python 3.9+ — dùng built-in types trực tiếp (khuyến khích)
names: list[str] = ["Alice", "Bob", "Charlie"]
scores: dict[str, int] = {"Alice": 95, "Bob": 87}
unique_ids: set[int] = {1, 2, 3}
coordinates: tuple[float, float] = (10.5, 20.3)

# Nested types
matrix: list[list[int]] = [[1, 2, 3], [4, 5, 6]]
config: dict[str, list[str]] = {"roles": ["admin", "user"]}
registry: dict[str, dict[str, int]] = {"user_1": {"age": 28, "score": 90}}

# Tuple với độ dài cố định — khai báo từng phần tử
point_2d: tuple[int, int] = (10, 20)
rgb: tuple[int, int, int] = (255, 128, 0)

# Tuple với độ dài biến đổi — dùng ...
coords: tuple[float, ...] = (1.0, 2.0, 3.0, 4.0)

# Python 3.8 trở về trước — phải import từ typing
from typing import List, Dict, Set, Tuple    # Vẫn hoạt động trong 3.12+
old_style: List[str] = ["Alice"]
```

---

## 2. `Union`, `Optional`, `Any` và Cú Pháp `X | Y`

### 2.1 `Optional` — Có Thể Là `None`

> **Java tương đương:** `Optional<T>` — nhưng Python dùng `Optional[T]` chỉ là type hint, không phải wrapper object như Java.

```python
from typing import Optional

# Optional[str] tương đương Union[str, None]
# Dùng khi giá trị có thể là None

def find_user(user_id: int) -> Optional[dict]:
    users = {1: {"name": "Alice"}, 2: {"name": "Bob"}}
    return users.get(user_id)   # Trả về None nếu không tìm thấy

result = find_user(1)
if result is not None:
    print(result["name"])   # Alice

# Tham số tùy chọn — thường kết hợp với default = None
def create_user(name: str, email: Optional[str] = None) -> dict:
    user = {"name": name}
    if email is not None:
        user["email"] = email
    return user

u1 = create_user("Alice")
u2 = create_user("Bob", "bob@example.com")
```

### 2.2 `Union` và Cú Pháp `X | Y` (Python 3.10+)

> **Python 3.10+ giới thiệu** cú pháp `X | Y` thay thế `Union[X, Y]` — ngắn gọn hơn nhiều.

```python
from typing import Union

# Python 3.9 trở về — dùng Union
def process_id(id: Union[int, str]) -> str:
    return str(id)

# Python 3.10+ — cú pháp | (khuyến khích dùng)
def process_id(id: int | str) -> str:
    return str(id)

# Optional[T] = Union[T, None] = T | None
def find_name(user_id: int) -> str | None:    # Python 3.10+ style
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)

# Union nhiều kiểu
def parse_value(raw: str | int | float | None) -> float | None:
    if raw is None:
        return None
    try:
        return float(raw)
    except (ValueError, TypeError):
        return None

print(parse_value("3.14"))     # 3.14
print(parse_value(42))         # 42.0
print(parse_value(None))       # None
print(parse_value("abc"))      # None
```

### 2.3 `Any` — Tắt Kiểm Tra Kiểu

> `Any` tương tự `Object` trong Java — nhưng với `Any`, mypy bỏ qua kiểm tra hoàn toàn. **Tránh dùng `Any` khi có thể** — nó làm mất lợi ích của type hints.

```python
from typing import Any

# Any — dùng khi thực sự không biết kiểu (ví dụ: dữ liệu JSON tùy ý)
def log_event(data: Any) -> None:
    print(f"[EVENT] {data}")

# Trường hợp hợp lý: xử lý JSON động
import json
def parse_json(raw: str) -> Any:
    return json.loads(raw)

parsed = parse_json('{"name": "Alice", "scores": [90, 85]}')
# parsed có kiểu Any — mypy không kiểm tra truy cập tiếp theo

# KHÔNG khuyến khích — dùng Any để tránh khai báo kiểu
def bad_function(x: Any, y: Any) -> Any:    # Vô nghĩa
    return x + y

# Nên dùng TypeVar (học ở phần sau) hoặc khai báo kiểu cụ thể
```

---

## 3. Annotating Functions — Khai Báo Kiểu Cho Tham Số và Return Type

### 3.1 Cú Pháp Đầy Đủ

> **Java tương đương:** Khai báo kiểu trả về và tham số trước tên — Python viết sau dấu `:` và `->`.

```python
# Java:
# public String formatGreeting(String name, int age) { ... }
# public Optional<User> findById(Long id) { ... }
# public void deleteUser(Long id) throws UserNotFoundException { ... }

# Python
def format_greeting(name: str, age: int) -> str:
    return f"Xin chào {name}, {age} tuổi!"

def find_by_id(user_id: int) -> dict | None:
    ...

def delete_user(user_id: int) -> None:    # None = void trong Java
    ...

# Hàm không bao giờ return (raise exception hoặc vòng lặp vô hạn)
from typing import NoReturn

def crash(message: str) -> NoReturn:
    raise RuntimeError(message)

def server_loop() -> NoReturn:
    while True:
        handle_request()
```

### 3.2 Default Parameters và `*args`, `**kwargs`

```python
from typing import Any

# Default parameter — khai báo kiểu như bình thường
def create_product(
    name: str,
    price: float,
    stock: int = 0,
    category: str = "general",
    is_active: bool = True,
) -> dict:
    return {
        "name": name,
        "price": price,
        "stock": stock,
        "category": category,
        "is_active": is_active,
    }

# *args — tuple của các tham số positional
def sum_all(*numbers: int) -> int:
    return sum(numbers)

print(sum_all(1, 2, 3, 4, 5))   # 15

# **kwargs — dict của các tham số keyword
def build_query(**filters: str | int) -> str:
    parts = [f"{k}={v}" for k, v in filters.items()]
    return "&".join(parts)

print(build_query(name="Alice", age=28, dept="Engineering"))
# name=Alice&age=28&dept=Engineering

# Kết hợp đầy đủ
def complex_func(
    required: str,
    optional: int = 0,
    *args: float,
    keyword_only: bool = False,   # Sau * → chỉ nhận theo tên
    **kwargs: Any,
) -> None:
    print(f"required={required}, optional={optional}")
    print(f"args={args}, keyword_only={keyword_only}, kwargs={kwargs}")

complex_func("hello", 1, 2.0, 3.0, keyword_only=True, extra="data")
```

### 3.3 `Callable` — Kiểu Cho Hàm

```python
from typing import Callable

# Callable[[param_types], return_type]
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

print(apply(lambda x, y: x + y, 3, 5))   # 8
print(apply(max, 10, 7))                  # 10

# Callable không quan tâm signature — dùng khi signature phức tạp
def run_callback(callback: Callable[..., None]) -> None:
    callback()

# Kết hợp với Optional — callback tùy chọn (pattern phổ biến)
def process_data(
    data: list[int],
    on_success: Callable[[list[int]], None] | None = None,
    on_error: Callable[[Exception], None] | None = None,
) -> list[int]:
    try:
        result = [x * 2 for x in data]
        if on_success:
            on_success(result)
        return result
    except Exception as e:
        if on_error:
            on_error(e)
        return []

process_data(
    [1, 2, 3],
    on_success=lambda r: print(f"OK: {r}"),
    on_error=lambda e: print(f"Error: {e}"),
)
```

---

## 4. Generic Types — `list[T]`, `dict[K, V]`, `Tuple[T, ...]`

### 4.1 `TypeVar` — Khai Báo Generic

> **Java tương đương:** `<T>`, `<K, V>` trong generics. Python dùng `TypeVar`.

```python
from typing import TypeVar

T = TypeVar("T")            # TypeVar tổng quát
K = TypeVar("K")            # Key
V = TypeVar("V")            # Value
N = TypeVar("N", int, float)  # Constrained — chỉ int hoặc float

# Hàm generic — hoạt động với bất kỳ kiểu nào
def first(items: list[T]) -> T | None:
    return items[0] if items else None

# Type inference — Python hiểu kiểu từ argument
x: int | None = first([1, 2, 3])        # T = int
y: str | None = first(["a", "b", "c"])  # T = str

# Generic với constraint
def add_numbers(a: N, b: N) -> N:
    return a + b

print(add_numbers(3, 4))       # 7 (int)
print(add_numbers(1.5, 2.5))   # 4.0 (float)
# add_numbers("a", "b")        # mypy báo lỗi — str không phải N
```

### 4.2 Generic Class

```python
from typing import TypeVar, Generic

T = TypeVar("T")

class Stack(Generic[T]):
    """Stack generic — tương tự Stack<T> trong Java."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("Stack rỗng")
        return self._items.pop()

    def peek(self) -> T | None:
        return self._items[-1] if self._items else None

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Stack({self._items})"

# Stack chứa int
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
int_stack.push(3)
print(int_stack.pop())   # 3
print(int_stack)         # Stack([1, 2])

# Stack chứa str
str_stack: Stack[str] = Stack()
str_stack.push("hello")
str_stack.push("world")
```

### 4.3 `Sequence`, `Mapping`, `Iterable` — Abstract Types

```python
from collections.abc import Sequence, Mapping, Iterable, Iterator

# Sequence — list-like: có index, len
# Rộng hơn list — chấp nhận list, tuple, str, range...
def process_items(items: Sequence[int]) -> int:
    return sum(items)

print(process_items([1, 2, 3]))     # Hoạt động với list
print(process_items((1, 2, 3)))     # Hoạt động với tuple
print(process_items(range(4)))      # Hoạt động với range

# Mapping — dict-like: key-value
def get_value(data: Mapping[str, int], key: str) -> int | None:
    return data.get(key)

# Iterable — bất kỳ thứ gì có thể duyệt bằng for
def print_all(items: Iterable[str]) -> None:
    for item in items:
        print(item)

print_all(["a", "b"])           # list
print_all(("x", "y"))           # tuple
print_all({"p", "q"})           # set
print_all(line.strip() for line in open("file.txt"))  # generator
```

---

## 5. `TypedDict` và `NamedTuple` — Khai Báo Cấu Trúc Có Kiểu

### 5.1 `TypedDict` — Dict Với Kiểu Cố Định

> **Java tương đương:** Gần với `Map<String, Object>` nhưng có kiểm tra kiểu từng key. Thực ra giống hơn với một DTO/record nhẹ.

```python
from typing import TypedDict, Required, NotRequired

# TypedDict — định nghĩa cấu trúc của một dict
class UserDict(TypedDict):
    id: int
    name: str
    email: str

# Python 3.11+ — Required/NotRequired
class ProductDict(TypedDict):
    id: int
    name: str
    price: float
    description: NotRequired[str]     # Không bắt buộc
    stock: NotRequired[int]

# Sử dụng
user: UserDict = {"id": 1, "name": "Alice", "email": "alice@example.com"}
print(user["name"])   # Alice

product: ProductDict = {"id": 10, "name": "Laptop", "price": 25_000_000}
# description và stock không bắt buộc — OK

# TypedDict vs dataclass:
# TypedDict — dùng khi làm việc với JSON/dict API (serialization/deserialization)
# dataclass — dùng khi cần object thực sự với methods và behavior

def format_user(user: UserDict) -> str:
    return f"[{user['id']}] {user['name']} <{user['email']}>"

# mypy kiểm tra key access
# user["unknown_key"]   # mypy báo lỗi — key không tồn tại trong TypedDict
```

### 5.2 `NamedTuple` — Tuple Với Tên Và Kiểu

> **Java tương đương:** `record` từ Java 16+ — immutable data holder với named fields.

```python
from typing import NamedTuple

# NamedTuple — tuple bất biến với tên field và kiểu
class Point(NamedTuple):
    x: float
    y: float
    label: str = ""   # Giá trị mặc định

class RGB(NamedTuple):
    red: int
    green: int
    blue: int

    def to_hex(self) -> str:
        return f"#{self.red:02X}{self.green:02X}{self.blue:02X}"

# Tạo instance
p1 = Point(3.0, 4.0)
p2 = Point(x=1.0, y=2.0, label="Origin")

print(p1.x, p1.y)       # 3.0 4.0
print(p1[0], p1[1])     # 3.0 4.0 — vẫn truy cập được qua index (là tuple)
print(len(p1))           # 2

# Immutable — không thể thay đổi
# p1.x = 5.0   # AttributeError

# Bất biến → hashable → dùng làm dict key
distances: dict[Point, float] = {
    Point(0, 0): 0.0,
    Point(3, 4): 5.0,
}

# NamedTuple hỗ trợ method
red = RGB(255, 0, 0)
print(red.to_hex())      # #FF0000

# Unpacking như tuple thường
x, y = p1
print(x, y)             # 3.0 4.0

# NamedTuple vs dataclass:
# NamedTuple — khi cần tuple-compatible, hashable, lightweight
# dataclass  — khi cần mutable, có logic phức tạp, kế thừa
```

---

## 6. Giới Thiệu Async Programming — Tại Sao Cần Async Trong API?

### 6.1 Vấn Đề Của Blocking I/O

> **Java developer:** Java truyền thống dùng thread-per-request (Servlet, Spring MVC). Mỗi request một thread — khi I/O chờ, thread bị block, không làm gì khác. Python (và Node.js, Go) dùng event loop — một thread xử lý nhiều request đồng thời nhờ async/await.

```python
import time

# Mô phỏng blocking I/O — như gọi database, HTTP request
def fetch_user_sync(user_id: int) -> dict:
    time.sleep(1)   # Giả lập I/O: 1 giây chờ
    return {"id": user_id, "name": f"User {user_id}"}

def fetch_product_sync(product_id: int) -> dict:
    time.sleep(1)   # Giả lập I/O: 1 giây chờ
    return {"id": product_id, "name": f"Product {product_id}"}

# Blocking — tuần tự, tổng thời gian = tổng thời gian từng task
start = time.perf_counter()

user    = fetch_user_sync(1)        # Chờ 1 giây
product = fetch_product_sync(10)    # Chờ thêm 1 giây

elapsed = time.perf_counter() - start
print(f"Sync: {elapsed:.2f}s")   # ~2.00s
```

```python
# So sánh throughput:
# Blocking server (Flask default):
#   - 1000 request × 100ms I/O = chỉ xử lý được ~10 req/s với 1 thread
#   - Phải scale bằng cách tăng thread/process (tốn RAM)
#
# Async server (FastAPI/Uvicorn):
#   - Trong khi chờ I/O, event loop xử lý request khác
#   - 1 thread có thể xử lý hàng nghìn concurrent I/O request
#   - FastAPI dùng async làm core → hiệu năng cao hơn Flask đáng kể
```

---

## 7. Tìm Hiểu `asyncio` — Event Loop, Coroutine, Task

### 7.1 Coroutine Là Gì?

> **Java developer:** Tương tự `CompletableFuture` / `Project Reactor` — nhưng cú pháp đơn giản hơn nhiều. Coroutine là hàm có thể **tạm dừng** và **tiếp tục** mà không block thread.

```python
import asyncio

# Coroutine function — định nghĩa bằng async def
async def say_hello(name: str) -> str:
    await asyncio.sleep(1)   # Tạm dừng 1 giây — KHÔNG block thread
    return f"Hello, {name}!"

# Coroutine object — gọi async def trả về coroutine, CHƯA chạy
coro = say_hello("Alice")
print(type(coro))   # <class 'coroutine'>

# Chạy coroutine bằng asyncio.run() — entry point chính
result = asyncio.run(say_hello("Bob"))
print(result)       # Hello, Bob!

# asyncio.run() làm 3 việc:
# 1. Tạo Event Loop mới
# 2. Chạy coroutine cho đến khi hoàn thành
# 3. Đóng Event Loop
```

### 7.2 Event Loop

```python
import asyncio

# Event Loop — trái tim của asyncio
# - Duy trì hàng đợi các task cần chạy
# - Khi task đang chờ I/O (await), event loop chuyển sang task khác
# - Khi I/O xong, event loop quay lại task cũ

async def demo_event_loop():
    print("Task A: bắt đầu")
    await asyncio.sleep(0.5)    # Nhường quyền cho event loop
    print("Task A: tiếp tục sau 0.5s")
    await asyncio.sleep(0.5)
    print("Task A: kết thúc")

async def demo_concurrent():
    # asyncio.gather() chạy nhiều coroutine ĐỒNG THỜI
    # Event loop luân phiên chạy khi từng coroutine await
    await asyncio.gather(
        demo_event_loop(),
        demo_event_loop(),
    )

asyncio.run(demo_concurrent())
# Task A: bắt đầu
# Task A: bắt đầu   ← cả hai đều bắt đầu trước khi cái nào sleep xong
# Task A: tiếp tục sau 0.5s
# Task A: tiếp tục sau 0.5s
# Task A: kết thúc
# Task A: kết thúc
```

### 7.3 `Task` — Lên Lịch Coroutine Chạy Song Song

```python
import asyncio

async def fetch_data(name: str, delay: float) -> str:
    print(f"  [{name}] Bắt đầu fetch...")
    await asyncio.sleep(delay)
    print(f"  [{name}] Hoàn thành sau {delay}s")
    return f"data từ {name}"

async def main():
    # Tạo Task — lên lịch coroutine chạy song song NGAY LẬP TỨC
    task_a = asyncio.create_task(fetch_data("ServiceA", 1.0))
    task_b = asyncio.create_task(fetch_data("ServiceB", 0.5))
    task_c = asyncio.create_task(fetch_data("ServiceC", 1.5))

    # Chờ tất cả task hoàn thành
    result_a = await task_a
    result_b = await task_b
    result_c = await task_c

    print(f"Kết quả: {result_a}, {result_b}, {result_c}")

import time
start = time.perf_counter()
asyncio.run(main())
elapsed = time.perf_counter() - start
print(f"Tổng thời gian: {elapsed:.2f}s")   # ~1.50s (không phải 1+0.5+1.5=3.0s)
```

---

## 8. `async def` và `await` — Viết Hàm Bất Đồng Bộ

### 8.1 Cú Pháp Cơ Bản

> **Java tương đương:** `async def` tương tự method trả về `CompletableFuture<T>`. `await` tương tự `.get()` nhưng không block thread — nhường quyền cho event loop.

```python
import asyncio
import httpx  # pip install httpx — HTTP client async (thay requests)

# async def — định nghĩa coroutine function
async def get_status(url: str) -> int:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)    # await — chờ không block
        return response.status_code

async def fetch_json(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()         # Raise nếu 4xx/5xx
        return response.json()

# Lồng async/await — gọi coroutine từ coroutine khác
async def fetch_user_and_posts(user_id: int) -> dict:
    user  = await fetch_json(f"https://jsonplaceholder.typicode.com/users/{user_id}")
    posts = await fetch_json(f"https://jsonplaceholder.typicode.com/posts?userId={user_id}")
    return {"user": user, "posts": posts}

# Chạy
result = asyncio.run(fetch_user_and_posts(1))
print(result["user"]["name"])
print(f"Số bài viết: {len(result['posts'])}")
```

### 8.2 `async with` và `async for`

```python
import asyncio
import aiofiles  # pip install aiofiles — async file I/O

# async with — context manager bất đồng bộ
async def write_log(message: str) -> None:
    async with aiofiles.open("async_log.txt", "a") as f:
        await f.write(f"{message}\n")

# async for — duyệt async iterator
async def read_lines(path: str):
    async with aiofiles.open(path, "r") as f:
        async for line in f:        # Đọc từng dòng bất đồng bộ
            yield line.strip()      # async generator

async def process_file():
    async for line in read_lines("async_log.txt"):
        print(f"  Line: {line}")

asyncio.run(process_file())
```

### 8.3 Exception Handling Trong Async

```python
import asyncio

async def risky_operation(n: int) -> int:
    await asyncio.sleep(0.1)
    if n == 0:
        raise ValueError("Không được bằng 0!")
    return 100 // n

async def safe_process(n: int) -> int | None:
    try:
        result = await risky_operation(n)
        return result
    except ValueError as e:
        print(f"Lỗi: {e}")
        return None
    except Exception as e:
        print(f"Lỗi không mong đợi: {e}")
        raise

async def main():
    results = await asyncio.gather(
        safe_process(5),    # OK → 20
        safe_process(0),    # ValueError → None
        safe_process(4),    # OK → 25
        return_exceptions=False,   # Mặc định — raise exception
    )
    print(results)

asyncio.run(main())

# return_exceptions=True → trả về exception như kết quả thay vì raise
async def main_safe():
    results = await asyncio.gather(
        risky_operation(5),
        risky_operation(0),    # Sẽ raise ValueError
        risky_operation(4),
        return_exceptions=True,
    )
    for r in results:
        if isinstance(r, Exception):
            print(f"  Exception: {r}")
        else:
            print(f"  OK: {r}")
```

---

## 9. So Sánh Blocking vs Non-blocking I/O

### 9.1 Benchmark Thực Tế

```python
import asyncio
import time
import httpx
import requests  # pip install requests — sync HTTP

URLS = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://jsonplaceholder.typicode.com/posts/3",
    "https://jsonplaceholder.typicode.com/posts/4",
    "https://jsonplaceholder.typicode.com/posts/5",
]

# --- CÁCH 1: Synchronous (Blocking) ---
def fetch_sync(url: str) -> dict:
    return requests.get(url).json()

def fetch_all_sync(urls: list[str]) -> list[dict]:
    return [fetch_sync(url) for url in urls]

start = time.perf_counter()
sync_results = fetch_all_sync(URLS)
sync_elapsed = time.perf_counter() - start
print(f"Sync:  {sync_elapsed:.2f}s — {len(sync_results)} results")

# --- CÁCH 2: Asynchronous (Non-blocking) ---
async def fetch_async(client: httpx.AsyncClient, url: str) -> dict:
    response = await client.get(url)
    return response.json()

async def fetch_all_async(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient() as client:
        tasks = [fetch_async(client, url) for url in urls]
        return await asyncio.gather(*tasks)

start = time.perf_counter()
async_results = asyncio.run(fetch_all_async(URLS))
async_elapsed = time.perf_counter() - start
print(f"Async: {async_elapsed:.2f}s — {len(async_results)} results")

# Kết quả điển hình với 5 URL (mỗi URL ~200ms):
# Sync:  ~1.00s  (5 × 0.2s — tuần tự)
# Async: ~0.25s  (chạy song song — chỉ mất thời gian của request chậm nhất)
```

### 9.2 Khi Nào Dùng Async — Khi Nào Không?

```python
# ✅ DÙNG ASYNC khi:
# - Gọi HTTP API bên ngoài (requests → httpx async)
# - Truy vấn database (SQLAlchemy async, asyncpg)
# - Đọc/ghi file lớn (aiofiles)
# - WebSocket, Server-Sent Events
# - Cần xử lý nhiều I/O đồng thời

# ❌ KHÔNG DÙNG ASYNC khi:
# - CPU-bound tasks (xử lý ảnh, mã hóa nặng, ML inference)
#   → Dùng ProcessPoolExecutor thay thế
# - Thư viện không hỗ trợ async (blocking library)
#   → Dùng run_in_executor

import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Chạy code blocking trong thread pool — không block event loop
async def run_blocking_in_thread():
    loop = asyncio.get_event_loop()

    # ThreadPoolExecutor — I/O blocking (GIL không ảnh hưởng I/O)
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool,
            lambda: requests.get("https://api.example.com/data").json()
        )
    return result

# ProcessPoolExecutor — CPU-bound tasks (bypass GIL)
def heavy_computation(n: int) -> int:
    return sum(i * i for i in range(n))   # CPU-bound

async def run_cpu_task():
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, heavy_computation, 10_000_000)
    return result
```

---

## 10. Bài Tập Async — Gọi Nhiều API Đồng Thời Bằng `asyncio.gather`

### 10.1 Pattern Cơ Bản

```python
import asyncio
import httpx
from typing import Any

BASE_URL = "https://jsonplaceholder.typicode.com"

async def fetch(client: httpx.AsyncClient, endpoint: str) -> Any:
    """Fetch một endpoint và trả về JSON."""
    response = await client.get(f"{BASE_URL}{endpoint}")
    response.raise_for_status()
    return response.json()

async def fetch_dashboard_data(user_id: int) -> dict:
    """
    Lấy dữ liệu dashboard cho user:
    - Thông tin user
    - Danh sách bài viết của user
    - Danh sách album của user
    Tất cả gọi đồng thời để tối ưu thời gian.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        user_task   = asyncio.create_task(fetch(client, f"/users/{user_id}"))
        posts_task  = asyncio.create_task(fetch(client, f"/posts?userId={user_id}"))
        albums_task = asyncio.create_task(fetch(client, f"/albums?userId={user_id}"))

        # Chờ tất cả hoàn thành
        user, posts, albums = await asyncio.gather(
            user_task, posts_task, albums_task
        )

    return {
        "user": {"id": user["id"], "name": user["name"], "email": user["email"]},
        "post_count": len(posts),
        "album_count": len(albums),
        "latest_post": posts[0]["title"] if posts else None,
    }

async def main():
    import time

    # Lấy dashboard cho nhiều user đồng thời
    start = time.perf_counter()

    dashboards = await asyncio.gather(
        fetch_dashboard_data(1),
        fetch_dashboard_data(2),
        fetch_dashboard_data(3),
    )

    elapsed = time.perf_counter() - start
    print(f"Tải {len(dashboards)} dashboard trong {elapsed:.2f}s\n")

    for dash in dashboards:
        print(f"  {dash['user']['name']}: "
              f"{dash['post_count']} bài, "
              f"{dash['album_count']} album")
        print(f"    Bài mới nhất: {dash['latest_post']}")

asyncio.run(main())
```

### 10.2 Timeout và Rate Limiting

```python
import asyncio
import httpx

async def fetch_with_timeout(
    client: httpx.AsyncClient,
    url: str,
    timeout: float = 5.0,
) -> dict | None:
    """Fetch với timeout — trả về None nếu quá timeout."""
    try:
        response = await asyncio.wait_for(
            client.get(url),
            timeout=timeout
        )
        return response.json()
    except asyncio.TimeoutError:
        print(f"  Timeout: {url}")
        return None
    except httpx.HTTPError as e:
        print(f"  HTTP Error: {url} — {e}")
        return None

async def fetch_with_semaphore(
    semaphore: asyncio.Semaphore,
    client: httpx.AsyncClient,
    url: str,
) -> dict | None:
    """Giới hạn số request đồng thời bằng Semaphore."""
    async with semaphore:   # Chỉ max N request chạy cùng lúc
        return await fetch_with_timeout(client, url)

async def fetch_many(urls: list[str], max_concurrent: int = 5) -> list[dict | None]:
    """Fetch nhiều URL với giới hạn concurrent và timeout."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async with httpx.AsyncClient() as client:
        tasks = [
            fetch_with_semaphore(semaphore, client, url)
            for url in urls
        ]
        return await asyncio.gather(*tasks)

# Test
urls = [
    f"https://jsonplaceholder.typicode.com/posts/{i}"
    for i in range(1, 21)   # 20 URL
]

import time
start = time.perf_counter()
results = asyncio.run(fetch_many(urls, max_concurrent=5))
elapsed = time.perf_counter() - start

successful = [r for r in results if r is not None]
print(f"\nKết quả: {len(successful)}/{len(urls)} thành công trong {elapsed:.2f}s")
```

### 10.3 Retry Pattern

```python
import asyncio
import httpx

async def fetch_with_retry(
    client: httpx.AsyncClient,
    url: str,
    max_retries: int = 3,
    backoff: float = 1.0,
) -> dict:
    """
    Fetch với retry và exponential backoff.
    Retry khi gặp 5xx hoặc network error.
    """
    last_error: Exception | None = None

    for attempt in range(1, max_retries + 1):
        try:
            response = await client.get(url, timeout=5.0)

            if response.status_code >= 500:
                # Server error — đáng retry
                raise httpx.HTTPStatusError(
                    f"Server error {response.status_code}",
                    request=response.request,
                    response=response,
                )

            response.raise_for_status()   # Raise cho 4xx
            return response.json()

        except (httpx.TimeoutException, httpx.NetworkError, httpx.HTTPStatusError) as e:
            last_error = e
            if attempt < max_retries:
                wait = backoff * (2 ** (attempt - 1))   # Exponential backoff
                print(f"  Attempt {attempt} failed: {e}. Retry sau {wait:.1f}s...")
                await asyncio.sleep(wait)
            else:
                print(f"  Attempt {attempt} failed: {e}. Hết lần retry.")

    raise RuntimeError(f"Không thể fetch {url} sau {max_retries} lần") from last_error

async def main():
    async with httpx.AsyncClient() as client:
        try:
            data = await fetch_with_retry(
                client,
                "https://jsonplaceholder.typicode.com/posts/1",
                max_retries=3,
            )
            print(f"OK: {data['title']}")
        except RuntimeError as e:
            print(f"Thất bại: {e}")

asyncio.run(main())
```

---

## Tóm Tắt — So Sánh Nhanh Java vs Python

| Khái niệm                | Java                                      | Python                                          |
|--------------------------|-------------------------------------------|-------------------------------------------------|
| Type system              | Static — bắt buộc khai báo               | Dynamic — type hints tùy chọn                  |
| Null safety              | `Optional<T>` wrapper object             | `T \| None` type hint (không wrap)              |
| Generics                 | `List<T>`, `Map<K, V>`                   | `list[T]`, `dict[K, V]` (3.9+)                 |
| Union type               | Không trực tiếp (`Object` hoặc interface) | `int \| str` (3.10+) / `Union[int, str]`        |
| Typed data structure     | POJO / `record`                           | `TypedDict` (dict) / `NamedTuple` (tuple)       |
| Async model              | Thread-per-request (servlet) / CompletableFuture / Project Reactor | `async/await` + `asyncio` event loop |
| Async keyword            | `CompletableFuture.supplyAsync()`         | `async def` + `await`                           |
| Run coroutine            | `.get()`, `.join()`                       | `asyncio.run(coroutine)`                        |
| Parallel async           | `CompletableFuture.allOf()`               | `asyncio.gather(*coroutines)`                   |
| Async context manager    | `try-with-resources`                      | `async with`                                    |
| Concurrent limit         | Semaphore / ThreadPoolExecutor            | `asyncio.Semaphore`                             |
| CPU-bound async          | ForkJoinPool / virtual threads (21+)      | `ProcessPoolExecutor` + `run_in_executor`       |

---

## Bài Tập Thực Hành

Tạo file `practice_08.py` và viết code cho các bài sau:

```python
# ============================================================
# PHẦN 1 — Type Hints
# ============================================================

# Bài 1: Annotate đầy đủ các hàm sau (thêm type hints cho tham số và return)
# Sau đó chạy: mypy practice_08.py để kiểm tra

from typing import TypeVar, NamedTuple
from collections.abc import Callable

T = TypeVar("T")

# 1a. Hàm tìm phần tử thỏa điều kiện
def find_first(items: list[T], predicate: Callable[[T], bool]) -> T | None:
    for item in items:
        if predicate(item):
            return item
    return None

evens = find_first([1, 3, 5, 6, 8], lambda x: x % 2 == 0)
print(f"Số chẵn đầu tiên: {evens}")   # 6

# 1b. Nhóm list theo key
def group_by(items: list[T], key: Callable[[T], str]) -> dict[str, list[T]]:
    result: dict[str, list[T]] = {}
    for item in items:
        k = key(item)
        result.setdefault(k, []).append(item)
    return result

words = ["apple", "banana", "avocado", "blueberry", "cherry", "apricot"]
grouped = group_by(words, lambda w: w[0])   # Nhóm theo chữ cái đầu
for letter, ws in sorted(grouped.items()):
    print(f"  {letter}: {ws}")

# 1c. TypedDict cho API response
from typing import TypedDict, NotRequired

class PaginatedResponse(TypedDict):
    data: list[dict]
    total: int
    page: int
    per_page: int
    has_next: NotRequired[bool]

def make_paginated(
    data: list[dict],
    page: int,
    per_page: int,
    total: int,
) -> PaginatedResponse:
    return {
        "data": data,
        "total": total,
        "page": page,
        "per_page": per_page,
        "has_next": (page * per_page) < total,
    }

response = make_paginated(
    data=[{"id": 1}, {"id": 2}],
    page=1,
    per_page=2,
    total=10,
)
print(f"Page {response['page']}, has_next={response.get('has_next')}")


# ============================================================
# PHẦN 2 — Async Programming
# ============================================================

import asyncio
import httpx
import time

# Bài 2: Fetch thông tin của 5 user từ JSONPlaceholder đồng thời
# - Mỗi user: lấy /users/{id} và /todos?userId={id}
# - Tính số todo đã hoàn thành (completed=True) cho mỗi user
# - In kết quả theo thứ tự hoàn thành

BASE = "https://jsonplaceholder.typicode.com"

async def fetch_user_stats(
    client: httpx.AsyncClient,
    user_id: int,
) -> dict:
    user, todos = await asyncio.gather(
        client.get(f"{BASE}/users/{user_id}"),
        client.get(f"{BASE}/todos?userId={user_id}"),
    )
    user_data  = user.json()
    todos_data = todos.json()

    completed = sum(1 for t in todos_data if t["completed"])
    return {
        "id": user_id,
        "name": user_data["name"],
        "total_todos": len(todos_data),
        "completed": completed,
        "completion_rate": f"{completed / len(todos_data) * 100:.0f}%",
    }

async def main():
    start = time.perf_counter()

    async with httpx.AsyncClient(timeout=10.0) as client:
        stats = await asyncio.gather(*[
            fetch_user_stats(client, uid) for uid in range(1, 6)
        ])

    elapsed = time.perf_counter() - start
    print(f"\nTải {len(stats)} users trong {elapsed:.2f}s\n")

    for s in stats:
        bar = "█" * (s["completed"] // 2)
        print(f"  [{s['id']}] {s['name']:<25} {bar:<10} "
              f"{s['completed']:>2}/{s['total_todos']} ({s['completion_rate']})")

asyncio.run(main())


# Bài 3: Async downloader với progress tracking
# - Download N URL đồng thời (max 3 concurrent)
# - Track và in tiến trình: "Xong 3/10 URL"
# - Báo cáo URL nào thất bại

async def download_with_progress(
    urls: list[str],
    max_concurrent: int = 3,
) -> dict[str, bool]:
    """Trả về dict {url: success}"""
    semaphore = asyncio.Semaphore(max_concurrent)
    results: dict[str, bool] = {}
    completed = 0
    total = len(urls)

    async def fetch_one(client: httpx.AsyncClient, url: str) -> None:
        nonlocal completed
        async with semaphore:
            try:
                response = await client.get(url, timeout=5.0)
                response.raise_for_status()
                results[url] = True
            except Exception:
                results[url] = False
            finally:
                completed += 1
                print(f"  Xong {completed}/{total} URL")

    async with httpx.AsyncClient() as client:
        await asyncio.gather(*[fetch_one(client, url) for url in urls])

    return results

test_urls = [
    f"https://jsonplaceholder.typicode.com/posts/{i}"
    for i in range(1, 11)
]

results = asyncio.run(download_with_progress(test_urls, max_concurrent=3))
success = sum(1 for ok in results.values() if ok)
print(f"\nKết quả: {success}/{len(test_urls)} thành công")
```
