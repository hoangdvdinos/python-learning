# integers
age = 30
big_number = 999_999_999_999_999_999_999
print(age)  # 30
print(big_number)  # 999999999999999999999

# floating point numbers
price = 19.99
scientific = 1.2e4
print(price)  # 19.99
print(scientific)  # 12000.0

# complex numbers
# research sau, 2 là thực, 3 là ảo
complex_number = 2 + 3j  
print(complex_number.real)   # 2.0
print(complex_number.imag)   # 3.0

# phép toán số học
# cộng trừ nhân chia giống java
# Lũy thừa khác nhau, java dùng Math.pow, python dùng **
squared = 5 ** 2
print(squared)  # 25

# Chia của thằng này sẽ trả về float, thằng java trả về int nếu cả hai là int
division = 10 / 3
print(division)  # 3.3333333333333335
# Chia lấy phần nguyên
floor_division = 10 // 3
print(floor_division)  # 3

# Chuyển đổi kiểu, ép kiểu
x = int(3.7)  # 3
y = float(5)  # 5.0
print(x)  # 3
print(y)  # 5.0
z = str(123)  # '123'
print(z)  # '123'
n = int("456")
print(n)  # 456

# Kiểm tra kiểu
print(type(age))  # <class 'int'>
print(isinstance(price, float))  # True

# Boolean
is_adult = age >= 18
print(is_adult)  # True
print(not isinstance(is_adult, bool))  # False

name = "Alice"
if name:
    print("Name is not empty")  # Name is not empty
else:
    print("Name is empty")
    
# bool là subclass của int, True = 1, False = 0
print(isinstance(True, int))  # True
print(True + True)  # 2
print(False + False)  # 0

# so sánh giá trị
print(10 == 10.0)  # True
print(10 is 10.0)  # False, vì là kiểu khác nhau
print("abc" == "abc")  # True
print("abc" is "abc")  # True, vì string literals thường được tối ưu

# chained comparison
print(1 < 2 < 3)  # True

a = [1, 2, 3] # tạo ra 1 ref mới
b = [1, 2, 3] # tạo ra 1 ref mới
c = a  # c trỏ đến cùng ref với a
print(a == b)  # True, vì giá trị giống nhau
print(a is b)  # False, vì a và b là hai đối tượng khác nhau
print(a is c)  # True, vì a và c trỏ đến cùng đối tượng

# None, dùng is để so sánh, không dùng == vì có thể có đối tượng khác cũng trả về False khi so sánh bằng ==
result = None
if result is None:
    print("Result is not available")  # Result is not available

# Toán tử in 
# Kiểm tra phần tử trong list
numbers = [1,2,3,4,5,6]
print(3 in numbers)
print(9 in numbers)

# Kiểm tra chuỗi con trong chuỗi
text= "Hello world"
print("world" in text)
print("python" in text)
print("java" not in text)

# Dictionary kiểm tra key
person = {"name": "Alice", "age": 30}
print("name" in person)  # True
print("height" in person)  # False

# Python and/or trả về giá trị gốc không phải boolean
print(1 and 2)
# -> phân tích cả 2 thằng đều truthy, nó chạy đến cuối cùng sau đó trả về 2
print(0 and 2)
# -> phân tích thằng đầu tiên là falsy, nó trả về 0 luôn mà không cần phân tích thằng thứ 2
# ứng dụng thực tế: gán giá trị mặc định
username = None
default_username = "guest"
current_username = username or default_username
print(current_username)  # guest

x = 10
x += 5  # x = 15
x -= 3  # x = 12
x *= 2  # x = 24
x /= 4  # x = 6.0
x %= 4  # x = 2.0
x **= 3  # x = 8.0
print(x)  # 8.0