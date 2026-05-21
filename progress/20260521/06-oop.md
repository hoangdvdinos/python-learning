# 06 — Lập Trình Hướng Đối Tượng (OOP)

> **Khối 5 — Lập Trình Hướng Đối Tượng (OOP)**
> Dành cho Java developer — tập trung vào điểm khác biệt so với Java.

---

## 1. Giới Thiệu OOP Trong Python — So Sánh Với Java

> Python là ngôn ngữ **multi-paradigm** — OOP không bắt buộc như Java. Bạn có thể viết hàm thuần túy, nhưng khi cần mô hình hóa thực thể phức tạp, OOP là lựa chọn phù hợp.

| Khía cạnh                  | Java                                     | Python                                      |
|----------------------------|------------------------------------------|---------------------------------------------|
| Mọi thứ đều là class?      | Có — ngay cả `main` phải trong class     | Không — class là tùy chọn                   |
| Access modifier            | `public`, `protected`, `private`         | Convention (`_`, `__`) — không enforce cứng |
| Interface                  | `interface` keyword                      | ABC hoặc Protocol (duck typing)             |
| Abstract class             | `abstract class`                         | `ABC` từ module `abc`                       |
| Overloading method         | Có — cùng tên, khác tham số             | Không — dùng default/`*args`                |
| Kiểu tĩnh                  | Bắt buộc khai báo                        | Tùy chọn (type hints)                       |
| Getter / Setter            | Phương thức `getX()` / `setX()`          | `@property` decorator                       |

---

## 2. Xây Dựng Class và Object — Thuộc Tính và Phương Thức

### 2.1 Cú Pháp Cơ Bản

> **Java developer chú ý:** Không có `new` keyword khi tạo object. Mọi phương thức instance đều phải có `self` là tham số đầu tiên (tương tự `this` của Java, nhưng tường minh hơn).

```python
# Java:
# public class Product {
#     private String name;
#     private double price;
#     public Product(String name, double price) { ... }
#     public String getName() { return name; }
# }

class Product:
    def __init__(self, name: str, price: float):
        self.name = name        # Instance attribute
        self.price = price

    def describe(self) -> str:
        return f"{self.name}: {self.price:,.0f} VND"

    def apply_discount(self, percent: float) -> None:
        self.price *= (1 - percent / 100)

# Tạo object — không có 'new'
laptop = Product("Laptop Dell", 25_000_000)
mouse  = Product("Mouse Logitech", 350_000)

print(laptop.describe())            # Laptop Dell: 25,000,000 VND
laptop.apply_discount(10)
print(laptop.describe())            # Laptop Dell: 22,500,000 VND

# Truy cập attribute trực tiếp (Java: phải qua getter)
print(laptop.name)                  # Laptop Dell
print(type(laptop))                 # <class '__main__.Product'>
print(isinstance(laptop, Product))  # True
```

### 2.2 Class Attribute vs Instance Attribute

> **Khác Java:** Class attribute dùng chung cho tất cả instance — tương tự `static` field trong Java, nhưng có thể bị "shadow" bởi instance attribute cùng tên.

```python
class BankAccount:
    interest_rate = 0.05    # Class attribute — dùng chung
    total_accounts = 0      # Class attribute — đếm tổng số tài khoản

    def __init__(self, owner: str, balance: float = 0):
        self.owner = owner      # Instance attribute
        self.balance = balance
        BankAccount.total_accounts += 1

    def get_annual_interest(self) -> float:
        return self.balance * BankAccount.interest_rate

acc1 = BankAccount("Alice", 10_000_000)
acc2 = BankAccount("Bob", 5_000_000)

print(BankAccount.total_accounts)   # 2 — class attribute
print(acc1.interest_rate)           # 0.05 — đọc từ class

# Gán trên instance → tạo instance attribute riêng, không ảnh hưởng class
acc1.interest_rate = 0.08
print(acc1.interest_rate)           # 0.08 — của riêng acc1
print(acc2.interest_rate)           # 0.05 — vẫn dùng class attribute
print(BankAccount.interest_rate)    # 0.05 — class không đổi
```

---

## 3. Constructor `__init__` và Destructor `__del__`

### 3.1 Constructor `__init__`

> **Java developer:** `__init__` tương tự constructor Java — nhưng Python chỉ có một constructor (không overload). Dùng default parameter để xử lý nhiều trường hợp.

```python
class DatabaseConnection:
    def __init__(self, host: str, port: int = 5432, database: str = "default"):
        self.host = host
        self.port = port
        self.database = database
        self._is_connected = False      # Convention: _ prefix = "nội bộ"
        print(f"[DB] Khởi tạo kết nối tới {host}:{port}/{database}")

    def connect(self):
        # Giả lập kết nối
        self._is_connected = True
        print(f"[DB] Đã kết nối tới {self.host}")

    def disconnect(self):
        self._is_connected = False
        print(f"[DB] Ngắt kết nối khỏi {self.host}")

db1 = DatabaseConnection("localhost")
db2 = DatabaseConnection("prod-server", port=3306, database="myapp")
```

```python
# __new__ — tạo object (hiếm khi override, khác Java không có tương đương trực tiếp)
# __init__ — khởi tạo state sau khi object đã được tạo
# Thứ tự: __new__ → __init__

class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: str):
        self.config = config

s1 = Singleton("config_A")
s2 = Singleton("config_B")
print(s1 is s2)         # True — cùng một object
print(s1.config)        # config_B — __init__ chạy lại, ghi đè config
```

### 3.2 Destructor `__del__`

> **Java developer:** Tương tự `finalize()` trong Java — **không nên dùng** để quản lý tài nguyên. Dùng **context manager** (`with` statement) thay thế.

```python
class FileHandler:
    def __init__(self, path: str):
        self.path = path
        self._file = open(path, "w", encoding="utf-8")
        print(f"[FILE] Mở file: {path}")

    def write(self, data: str):
        self._file.write(data)

    def __del__(self):
        if not self._file.closed:
            self._file.close()
            print(f"[FILE] Đóng file: {self.path} (từ __del__)")

# __del__ được gọi khi object bị garbage collect — KHÔNG đảm bảo thời điểm
# → Dùng context manager thay thế:

class BetterFileHandler:
    def __init__(self, path: str):
        self.path = path
        self._file = None

    def __enter__(self):
        self._file = open(self.path, "w", encoding="utf-8")
        print(f"[FILE] Mở: {self.path}")
        return self

    def write(self, data: str):
        self._file.write(data)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file:
            self._file.close()
            print(f"[FILE] Đóng: {self.path}")
        return False    # Không suppress exception

with BetterFileHandler("output.txt") as fh:
    fh.write("Hello, World!\n")
# File tự động đóng khi ra khỏi with block — dù có exception hay không
```

---

## 4. Tính Đóng Gói — Public, Protected, Private

> **Điểm khác biệt lớn nhất so với Java:** Python **không enforce** access control ở cấp ngôn ngữ — chỉ dùng **convention** (quy ước đặt tên).

### 4.1 Ba Mức Truy Cập

```python
class Employee:
    # Public — truy cập từ mọi nơi (giống public Java)
    name: str

    # Protected — convention: _ prefix
    # "Nội bộ và subclass" — nhưng KHÔNG bị ngăn nếu truy cập từ ngoài
    _salary: float

    # Private — convention: __ prefix (name mangling)
    # Python đổi tên thành _ClassName__attr → khó truy cập nhưng KHÔNG impossible
    __id: str

    def __init__(self, name: str, salary: float, emp_id: str):
        self.name = name
        self._salary = salary
        self.__id = emp_id

    def get_info(self) -> str:
        return f"{self.name} | ID: {self.__id} | Lương: {self._salary:,}"

emp = Employee("Hoàng", 25_000_000, "EMP-001")

print(emp.name)             # Hoàng — OK, public
print(emp._salary)          # 25000000 — OK (kỹ thuật), nhưng vi phạm convention
# print(emp.__id)           # AttributeError — name mangling

# Name mangling: __id → _Employee__id
print(emp._Employee__id)    # EMP-001 — vẫn truy cập được nếu biết tên
```

### 4.2 `@property` — Getter và Setter Pythonic

> **Java tương đương:** `getX()` / `setX()` — nhưng Python dùng attribute syntax thay vì method call.

```python
class Temperature:
    def __init__(self, celsius: float):
        self._celsius = celsius     # Lưu trữ nội bộ

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError(f"Nhiệt độ không thể dưới -273.15°C, nhận: {value}")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self.celsius = (value - 32) * 5/9  # Dùng lại validation của celsius.setter

    @property
    def kelvin(self) -> float:
        return self._celsius + 273.15

temp = Temperature(100)
print(temp.celsius)         # 100 — gọi như attribute
print(temp.fahrenheit)      # 212.0
print(temp.kelvin)          # 373.15

temp.celsius = 0            # Gọi setter
print(temp.fahrenheit)      # 32.0

temp.fahrenheit = 32        # Gọi fahrenheit.setter → celsius.setter
print(temp.celsius)         # 0.0

try:
    temp.celsius = -300     # ValueError
except ValueError as e:
    print(f"Lỗi: {e}")
```

---

## 5. Tính Kế Thừa P1 — Đơn Kế Thừa

> **Java tương đương:** `extends` — nhưng Python dùng cú pháp `class Child(Parent):`.

### 5.1 Cú Pháp Kế Thừa

```python
class Animal:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def speak(self) -> str:
        return f"{self.name} phát ra âm thanh"

    def describe(self) -> str:
        return f"{self.name} ({self.age} tuổi)"

class Dog(Animal):
    def __init__(self, name: str, age: int, breed: str):
        super().__init__(name, age)     # Gọi constructor của parent
        self.breed = breed

    def speak(self) -> str:            # Override phương thức
        return f"{self.name} sủa: Gâu gâu!"

    def fetch(self) -> str:
        return f"{self.name} chạy đi nhặt bóng"

class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} kêu: Meo meo!"

dog = Dog("Rex", 3, "Labrador")
cat = Cat("Whiskers", 5)

print(dog.speak())          # Rex sủa: Gâu gâu!
print(dog.describe())       # Rex (3 tuổi) — kế thừa từ Animal
print(dog.fetch())          # Rex chạy đi nhặt bóng
print(cat.speak())          # Whiskers kêu: Meo meo!

# isinstance kiểm tra chuỗi kế thừa
print(isinstance(dog, Dog))     # True
print(isinstance(dog, Animal))  # True — Dog là Animal
print(isinstance(dog, Cat))     # False
```

### 5.2 Kiểm Tra Quan Hệ Kế Thừa

```python
print(issubclass(Dog, Animal))      # True
print(issubclass(Dog, Cat))         # False
print(issubclass(Animal, object))   # True — mọi class Python đều kế thừa object

# Xem chuỗi kế thừa (MRO — sẽ học kỹ ở phần đa kế thừa)
print(Dog.__mro__)
# (<class 'Dog'>, <class 'Animal'>, <class 'object'>)
```

---

## 6. Tính Kế Thừa P2 — Override và `super()`

### 6.1 Override Phương Thức

```python
class Shape:
    def __init__(self, color: str = "white"):
        self.color = color

    def area(self) -> float:
        raise NotImplementedError("Subclass phải implement area()")

    def perimeter(self) -> float:
        raise NotImplementedError("Subclass phải implement perimeter()")

    def describe(self) -> str:
        return (f"{self.__class__.__name__} màu {self.color}: "
                f"diện tích={self.area():.2f}, chu vi={self.perimeter():.2f}")

import math

class Circle(Shape):
    def __init__(self, radius: float, color: str = "white"):
        super().__init__(color)     # Gọi Shape.__init__
        self.radius = radius

    def area(self) -> float:        # Override
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:   # Override
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, width: float, height: float, color: str = "white"):
        super().__init__(color)
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

shapes = [
    Circle(5, "red"),
    Rectangle(4, 6, "blue"),
    Circle(3),
]

for shape in shapes:
    print(shape.describe())
# Circle màu red: diện tích=78.54, chu vi=31.42
# Rectangle màu blue: diện tích=24.00, chu vi=20.00
# Circle màu white: diện tích=28.27, chu vi=18.85
```

### 6.2 `super()` — Gọi Phương Thức Của Parent

> **Java tương đương:** `super.method()` — Python dùng `super().method()` không cần tên class cha.

```python
class Vehicle:
    def __init__(self, brand: str, speed: float):
        self.brand = brand
        self.speed = speed

    def info(self) -> str:
        return f"{self.brand} (tốc độ tối đa: {self.speed} km/h)"

class ElectricVehicle(Vehicle):
    def __init__(self, brand: str, speed: float, battery_kwh: float):
        super().__init__(brand, speed)      # Gọi Vehicle.__init__
        self.battery_kwh = battery_kwh

    def info(self) -> str:
        base_info = super().info()          # Gọi Vehicle.info()
        return f"{base_info} | Pin: {self.battery_kwh} kWh"

class ElectricCar(ElectricVehicle):
    def __init__(self, brand: str, speed: float, battery_kwh: float, seats: int):
        super().__init__(brand, speed, battery_kwh)   # Gọi ElectricVehicle.__init__
        self.seats = seats

    def info(self) -> str:
        base_info = super().info()          # Gọi ElectricVehicle.info()
        return f"{base_info} | {self.seats} chỗ ngồi"

tesla = ElectricCar("Tesla Model 3", 250, 75, 5)
print(tesla.info())
# Tesla Model 3 (tốc độ tối đa: 250 km/h) | Pin: 75 kWh | 5 chỗ ngồi
```

---

## 7. Đa Kế Thừa và MRO

> **Java không có đa kế thừa class** (chỉ đa kế thừa interface). Python cho phép, nhưng cần hiểu MRO để tránh diamond problem.

### 7.1 Cú Pháp Đa Kế Thừa

```python
class Flyable:
    def fly(self) -> str:
        return f"{self.__class__.__name__} đang bay"

    def describe(self) -> str:
        return "Có thể bay"

class Swimmable:
    def swim(self) -> str:
        return f"{self.__class__.__name__} đang bơi"

    def describe(self) -> str:
        return "Có thể bơi"

class Duck(Flyable, Swimmable):     # Kế thừa từ cả hai
    def quack(self) -> str:
        return "Quack quack!"

duck = Duck()
print(duck.fly())       # Duck đang bay
print(duck.swim())      # Duck đang bơi
print(duck.quack())     # Quack quack!
print(duck.describe())  # Có thể bay — lấy từ Flyable (MRO)
```

### 7.2 MRO — Method Resolution Order

> Python dùng thuật toán **C3 Linearization** để xác định thứ tự tìm kiếm phương thức. Quy tắc đơn giản: từ trái sang phải, con trước cha.

```python
class A:
    def hello(self): return "A"

class B(A):
    def hello(self): return "B"

class C(A):
    def hello(self): return "C"

class D(B, C):
    pass

d = D()
print(d.hello())        # B — tìm theo MRO: D → B → C → A
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

# Xem MRO dễ đọc hơn
for cls in D.__mro__:
    print(cls.__name__, end=" → ")
# D → B → C → A → object →
```

```python
# super() trong đa kế thừa — gọi theo MRO, không phải class cụ thể
class Base:
    def __init__(self):
        print("Base.__init__")

class Left(Base):
    def __init__(self):
        print("Left.__init__")
        super().__init__()  # Gọi theo MRO — không phải Base trực tiếp

class Right(Base):
    def __init__(self):
        print("Right.__init__")
        super().__init__()

class Child(Left, Right):
    def __init__(self):
        print("Child.__init__")
        super().__init__()

Child()
# Child.__init__
# Left.__init__
# Right.__init__
# Base.__init__
# Mỗi class chỉ được gọi một lần — MRO đảm bảo không bị gọi lặp
```

---

## 8. Tính Đa Hình và Duck Typing

### 8.1 Polymorphism

> **Java:** Polymorphism thông qua interface hoặc abstract class — kiểu tĩnh.  
> **Python:** Polymorphism tự nhiên — không cần khai báo interface.

```python
class Dog:
    def speak(self) -> str: return "Gâu gâu!"

class Cat:
    def speak(self) -> str: return "Meo meo!"

class Parrot:
    def speak(self) -> str: return "Chào bạn! Chào bạn!"

# Không cần interface chung — chỉ cần cùng tên phương thức
animals = [Dog(), Cat(), Parrot()]

for animal in animals:
    print(f"{animal.__class__.__name__}: {animal.speak()}")
# Dog: Gâu gâu!
# Cat: Meo meo!
# Parrot: Chào bạn! Chào bạn!
```

### 8.2 Duck Typing

> "Nếu nó đi như vịt và kêu như vịt, thì nó là vịt." — Python không kiểm tra kiểu, chỉ kiểm tra hành vi.

```python
# Hàm này hoạt động với BẤT KỲ đối tượng nào có phương thức .write()
def save_data(writer, data: str) -> None:
    writer.write(data)      # Duck typing — không quan tâm kiểu cụ thể

class FileWriter:
    def write(self, data: str) -> None:
        print(f"[FILE] Ghi: {data}")

class DatabaseWriter:
    def write(self, data: str) -> None:
        print(f"[DB] INSERT: {data}")

class NetworkWriter:
    def write(self, data: str) -> None:
        print(f"[NET] Gửi: {data}")

# Dùng với bất kỳ "writer" nào
save_data(FileWriter(), "record_001")       # [FILE] Ghi: record_001
save_data(DatabaseWriter(), "record_001")   # [DB] INSERT: record_001
save_data(NetworkWriter(), "record_001")    # [NET] Gửi: record_001
```

### 8.3 Abstract Base Class (ABC)

> Khi muốn **ép buộc** subclass implement phương thức cụ thể (giống `abstract` Java):

```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def charge(self, amount: float) -> bool:
        pass

    @abstractmethod
    def refund(self, amount: float) -> bool:
        pass

    def receipt(self, amount: float) -> str:    # Phương thức cụ thể — có thể override
        return f"Giao dịch: {amount:,.0f} VND"

class CreditCard(PaymentMethod):
    def charge(self, amount: float) -> bool:
        print(f"[CC] Thanh toán {amount:,.0f} VND")
        return True

    def refund(self, amount: float) -> bool:
        print(f"[CC] Hoàn tiền {amount:,.0f} VND")
        return True

class MoMo(PaymentMethod):
    def charge(self, amount: float) -> bool:
        print(f"[MoMo] Thanh toán {amount:,.0f} VND")
        return True

    def refund(self, amount: float) -> bool:
        print(f"[MoMo] Hoàn tiền {amount:,.0f} VND")
        return True

# PaymentMethod() → TypeError: Can't instantiate abstract class
# CreditCard thiếu refund() → TypeError khi khởi tạo

cc = CreditCard()
cc.charge(500_000)
print(cc.receipt(500_000))
```

---

## 9. Dunder Methods

> **Dunder (Double Underscore)** = magic methods — Python gọi tự động trong các tình huống cụ thể. **Java tương đương:** Override `toString()`, `equals()`, `hashCode()`, `compareTo()`.

### 9.1 `__str__` và `__repr__`

```python
class Product:
    def __init__(self, name: str, price: float, stock: int):
        self.name = name
        self.price = price
        self.stock = stock

    def __repr__(self) -> str:
        # Dùng cho debug — nên có thể tái tạo object
        # Java: không có tương đương chuẩn
        return f"Product(name={self.name!r}, price={self.price}, stock={self.stock})"

    def __str__(self) -> str:
        # Dùng cho hiển thị người dùng — Java: toString()
        return f"{self.name} | {self.price:,.0f} VND | Còn {self.stock} cái"

p = Product("Laptop", 25_000_000, 5)

print(p)            # Gọi __str__: Laptop | 25,000,000 VND | Còn 5 cái
print(repr(p))      # Gọi __repr__: Product(name='Laptop', price=25000000, stock=5)
print(f"{p!r}")     # Ép dùng __repr__ trong f-string
print(f"{p}")       # Dùng __str__ (mặc định)

# Trong list/dict — Python gọi __repr__ (không phải __str__)
products = [Product("Mouse", 350_000, 20)]
print(products)     # [Product(name='Mouse', price=350000, stock=20)]
```

### 9.2 `__len__`, `__eq__`, `__lt__`

```python
class Playlist:
    def __init__(self, name: str):
        self.name = name
        self._songs: list[str] = []

    def add(self, song: str) -> None:
        self._songs.append(song)

    def __len__(self) -> int:
        # Cho phép dùng len(playlist)
        return len(self._songs)

    def __eq__(self, other: object) -> bool:
        # Java: equals() — so sánh bằng nội dung
        if not isinstance(other, Playlist):
            return NotImplemented
        return self._songs == other._songs

    def __contains__(self, song: str) -> bool:
        # Cho phép dùng 'song in playlist'
        return song in self._songs

    def __getitem__(self, index: int) -> str:
        # Cho phép dùng playlist[i]
        return self._songs[index]

    def __repr__(self) -> str:
        return f"Playlist({self.name!r}, {len(self)} bài)"

pl1 = Playlist("Chill")
pl1.add("Shape of You")
pl1.add("Blinding Lights")

print(len(pl1))                         # 2
print("Shape of You" in pl1)            # True
print(pl1[0])                           # Shape of You
print(pl1)                              # Playlist('Chill', 2 bài)

pl2 = Playlist("Study")
pl2.add("Shape of You")
pl2.add("Blinding Lights")
print(pl1 == pl2)                       # True — cùng nội dung
```

### 9.3 `__add__`, `__mul__` — Operator Overloading

```python
class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector":
        return self.__mul__(scalar)     # 3 * v và v * 3 đều hoạt động

    def __abs__(self) -> float:
        import math
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)

print(v1 + v2)      # Vector(4, 6)
print(v2 - v1)      # Vector(2, 2)
print(v1 * 3)       # Vector(3, 6)
print(3 * v1)       # Vector(3, 6) — nhờ __rmul__
print(abs(v2))      # 5.0
```

---

## 10. Dataclass — Thay Thế Class Thuần Túy Lưu Dữ Liệu

> `@dataclass` tự động sinh `__init__`, `__repr__`, `__eq__` — tương tự **Lombok** trong Java hoặc **Record** từ Java 16+.

### 10.1 Cú Pháp Cơ Bản

```python
from dataclasses import dataclass, field

# Không dùng @dataclass — phải viết tay
class ProductManual:
    def __init__(self, name: str, price: float, stock: int = 0):
        self.name = name
        self.price = price
        self.stock = stock

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price}, stock={self.stock})"

    def __eq__(self, other):
        if not isinstance(other, ProductManual): return NotImplemented
        return (self.name, self.price, self.stock) == (other.name, other.price, other.stock)

# Dùng @dataclass — tự động sinh tất cả
@dataclass
class Product:
    name: str
    price: float
    stock: int = 0              # Default value

p1 = Product("Laptop", 25_000_000, 5)
p2 = Product("Laptop", 25_000_000, 5)

print(p1)               # Product(name='Laptop', price=25000000, stock=5)
print(p1 == p2)         # True — __eq__ tự động so sánh từng field
```

### 10.2 Tùy Chỉnh Dataclass

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass(order=True, frozen=False)
class Employee:
    # order=True → sinh __lt__, __le__, __gt__, __ge__ (so sánh theo thứ tự field)
    # frozen=True → immutable (giống Java record)

    sort_index: float = field(init=False, repr=False)   # Không nhận trong __init__

    name: str
    department: str
    salary: float
    hire_date: datetime = field(default_factory=datetime.now)
    skills: list[str] = field(default_factory=list)     # Mutable default — dùng field()

    def __post_init__(self):
        # Chạy sau __init__ — dùng để validate hoặc tính toán
        if self.salary < 0:
            raise ValueError("Lương không thể âm")
        self.sort_index = self.salary   # Sắp xếp theo lương

    def add_skill(self, skill: str) -> None:
        self.skills.append(skill)

e1 = Employee("Alice", "Engineering", 35_000_000)
e2 = Employee("Bob", "Engineering", 40_000_000)
e1.add_skill("Python")
e1.add_skill("FastAPI")

print(e1)
# Employee(name='Alice', department='Engineering', salary=35000000, ...)

print(e1 < e2)          # True — so sánh theo sort_index (salary)

# Sắp xếp list employee theo lương
team = [e2, e1, Employee("Charlie", "Marketing", 28_000_000)]
team.sort()
for emp in team:
    print(f"{emp.name}: {emp.salary:,}")
```

### 10.3 Khi Nào Dùng Dataclass?

```python
# Dùng @dataclass khi:
# - Class chủ yếu để lưu dữ liệu (data container)
# - Cần __init__, __repr__, __eq__ tự động
# - Tương đương Java: POJO, DTO, Record

# Dùng class thường khi:
# - Class có logic phức tạp
# - Cần kiểm soát chặt __init__ (validation đặc biệt, side effects)
# - Kế thừa phức tạp

# Frozen dataclass — immutable, dùng làm dict key hoặc trong set
@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
# p.x = 3.0     # FrozenInstanceError

# Vì frozen=True → có __hash__ → dùng được trong set/dict
points = {Point(0, 0), Point(1, 1), Point(0, 0)}
print(len(points))  # 2 — trùng nhau tự loại
```

---

## Tóm Tắt — So Sánh Nhanh Java vs Python OOP

| Khái niệm              | Java                                   | Python                                     |
|------------------------|----------------------------------------|--------------------------------------------|
| Khai báo class         | `public class Foo { }`                 | `class Foo:`                               |
| Constructor            | `public Foo(params) { }`              | `def __init__(self, params):`              |
| Tạo object             | `Foo obj = new Foo()`                 | `obj = Foo()`                              |
| `this`                 | Ngầm định                              | `self` — tường minh, là tham số đầu tiên   |
| Kế thừa                | `class B extends A`                   | `class B(A):`                              |
| Gọi phương thức cha    | `super.method()`                       | `super().method()`                         |
| Access control         | `public/protected/private` — cứng      | `_` / `__` — convention                   |
| Getter/Setter          | `getX()` / `setX()`                   | `@property` / `@x.setter`                 |
| toString               | `@Override String toString()`         | `def __str__(self):`                       |
| equals                 | `@Override boolean equals(Object o)`  | `def __eq__(self, other):`                 |
| Đa kế thừa             | Không (chỉ interface)                  | Có — dùng MRO                              |
| Abstract class         | `abstract class`                       | `class X(ABC):` + `@abstractmethod`       |
| POJO/DTO               | Lombok `@Data`                         | `@dataclass`                               |
| Immutable class        | `record` (Java 16+), `final` fields   | `@dataclass(frozen=True)`                 |
| Operator overloading   | Không                                  | Dunder methods (`__add__`, `__mul__`...)   |

---

## Bài Tập Thực Hành

Tạo file `practice_06.py` và viết code cho các bài sau:

```python
# ============================================================
# PHẦN 1 — Class Cơ Bản, Property, Encapsulation
# ============================================================

# Bài 1: Xây dựng class BankAccount
# - Thuộc tính: owner (str), _balance (float, không âm), _transactions (list)
# - @property balance — chỉ đọc
# - deposit(amount) — kiểm tra amount > 0
# - withdraw(amount) — kiểm tra đủ tiền
# - get_statement() — in lịch sử giao dịch
from dataclasses import dataclass, field
from datetime import datetime

class BankAccount:
    def __init__(self, owner: str, initial_balance: float = 0):
        if initial_balance < 0:
            raise ValueError("Số dư ban đầu không thể âm")
        self.owner = owner
        self._balance = initial_balance
        self._transactions: list[dict] = []
        if initial_balance > 0:
            self._transactions.append({"type": "OPEN", "amount": initial_balance, "time": datetime.now()})

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Số tiền nạp phải dương")
        self._balance += amount
        self._transactions.append({"type": "DEPOSIT", "amount": amount, "time": datetime.now()})
        print(f"[+] Nạp {amount:,.0f} VND | Số dư: {self._balance:,.0f} VND")

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Số tiền rút phải dương")
        if amount > self._balance:
            raise ValueError(f"Không đủ tiền — số dư: {self._balance:,.0f} VND")
        self._balance -= amount
        self._transactions.append({"type": "WITHDRAW", "amount": -amount, "time": datetime.now()})
        print(f"[-] Rút {amount:,.0f} VND | Số dư: {self._balance:,.0f} VND")

    def get_statement(self) -> None:
        print(f"\n=== Sao kê tài khoản: {self.owner} ===")
        for tx in self._transactions:
            sign = "+" if tx["amount"] >= 0 else ""
            print(f"  {tx['type']:10} | {sign}{tx['amount']:>15,.0f} VND | {tx['time'].strftime('%H:%M:%S')}")
        print(f"  {'Số dư hiện tại':10} | {self._balance:>15,.0f} VND")

acc = BankAccount("Hoàng", 10_000_000)
acc.deposit(5_000_000)
acc.withdraw(3_000_000)
acc.get_statement()


# ============================================================
# PHẦN 2 — Kế Thừa, Polymorphism, ABC
# ============================================================

# Bài 2: Hệ thống hình học
# - Abstract class Shape với abstract method area(), perimeter()
# - Implement: Circle, Rectangle, Triangle
# - Hàm total_area(shapes) dùng duck typing
from abc import ABC, abstractmethod
import math

class Shape(ABC):
    def __init__(self, color: str = "white"):
        self.color = color

    @abstractmethod
    def area(self) -> float: pass

    @abstractmethod
    def perimeter(self) -> float: pass

    def __str__(self) -> str:
        return (f"{self.__class__.__name__}({self.color}): "
                f"S={self.area():.2f}, P={self.perimeter():.2f}")

class Circle(Shape):
    def __init__(self, radius: float, color: str = "white"):
        super().__init__(color)
        self.radius = radius
    def area(self): return math.pi * self.radius ** 2
    def perimeter(self): return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, w: float, h: float, color: str = "white"):
        super().__init__(color)
        self.w, self.h = w, h
    def area(self): return self.w * self.h
    def perimeter(self): return 2 * (self.w + self.h)

class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float, color: str = "white"):
        super().__init__(color)
        self.a, self.b, self.c = a, b, c
    def area(self):
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
    def perimeter(self): return self.a + self.b + self.c

def total_area(shapes: list) -> float:
    return sum(s.area() for s in shapes)

shapes = [Circle(5, "red"), Rectangle(4, 6, "blue"), Triangle(3, 4, 5)]
for s in shapes:
    print(s)
print(f"Tổng diện tích: {total_area(shapes):.2f}")


# ============================================================
# PHẦN 3 — Dunder Methods, Dataclass
# ============================================================

# Bài 3: Dataclass cho hệ thống quản lý nhân viên
@dataclass(order=True)
class Department:
    sort_index: str = field(init=False, repr=False)
    name: str
    budget: float
    employees: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.sort_index = self.name

    def add_employee(self, name: str) -> None:
        self.employees.append(name)

    def __len__(self) -> int:
        return len(self.employees)

    def __contains__(self, name: str) -> bool:
        return name in self.employees

eng = Department("Engineering", 500_000_000)
mkt = Department("Marketing", 200_000_000)

eng.add_employee("Alice")
eng.add_employee("Bob")
eng.add_employee("Charlie")
mkt.add_employee("Dave")

print(f"Engineering: {len(eng)} nhân viên")
print("Alice" in eng)   # True
print("Dave" in eng)    # False

departments = [mkt, eng]
departments.sort()
for dept in departments:
    print(f"{dept.name}: {len(dept)} người | ngân sách: {dept.budget:,} VND")
```
