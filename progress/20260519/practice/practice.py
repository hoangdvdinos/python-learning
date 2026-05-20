# square = lambda x: x ** 2
# print(square(5))  # 25

# # filter simulate
# def my_filter(func, iterable):
#     result = []
#     for item in iterable:
#         if func(item):
#             result.append(item)
#     return result

# # filter example
# numbers = [1, 2, 3, 4, 5, 6]
# even_numbers = my_filter(lambda x: x % 2 == 0, numbers)
# print(even_numbers)  # [2, 4, 6]

# mixed = [0, 1, "", "hello", None, True, False, [], [1, 2]]
# truthy = list(filter(lambda x: bool(x), mixed))
# print(truthy)       # [1, 'hello', True, [1, 2]]

# counter = 0

# def increment():
#     global counter      # Khai báo muốn sửa biến global
#     counter += 1

# increment()
# increment()
# print(counter)  # 2

# # Không có global — Python tạo biến local mới
# def increment_wrong():
#     counter += 1    # UnboundLocalError — Python thấy có phép gán nên coi là local
#                     # nhưng local chưa được khởi tạo trước khi += 1
# increment_wrong()  # UnboundLocalError: local variable 'counter' referenced before assignment
# print(counter)  # 2 (counter không bị thay đổi)

# # Dựng Iterator
# class CountDown:
#     def __init__(self, start):
#         self.current = start
    
#     def __iter__(self):
#         return self
    
#     def __next__(self):
#         if self.current < 0:
#             raise StopIteration
#         value = self.current
#         self.current -= 1
#         return value
# # Sử dụng CountDown
# for number in CountDown(5):
#     print(number)

# def get_squares_list(n):
#     return [x ** 2 for x in range(n)]

# def get_squares_generator(n):
#     for x in range(n):
#         yield x ** 2
# squares_gen = get_squares_generator(1_000_000)
# print(squares_gen)  # 0

# data = range(1, 1000001)
# filtered = (n for n in data if n % 2 == 0)     # Chỉ số chẵn
# squared  = (n ** 2 for n in filtered)           # Bình phương
# result   = sum(n for n in squared if n < 1000) 
# print(result)

# from functools import wraps
# import time

# # Không dùng wraps → mất metadata của hàm gốc
# def timer(func):
#     # @wraps(func)    # Giữ nguyên __name__, __doc__ của hàm gốc
#     def wrapper(*args, **kwargs):
#         start = time.perf_counter()
#         result = func(*args, **kwargs)
#         elapsed = time.perf_counter() - start
#         print(f"[TIMER] {func.__name__} chạy trong {elapsed:.4f}s")
#         return result
#     return wrapper

# @timer
# def slow_sum(n):
#     """Tính tổng từ 1 đến n."""
#     return sum(range(n + 1))

# result = slow_sum(1_000_000)
# print(result)
# print(slow_sum.__name__)    # slow_sum (giữ tên gốc nhờ @wraps)
# print(slow_sum.__doc__)     # Tính tổng từ 1 đến n.

# ============================================================
# PHẦN 1 — Xây Dựng Hàm
# ============================================================

# Bài 1: Hàm với tham số linh hoạt
# Viết hàm tính trung bình, hỗ trợ:
# - Bỏ qua N phần tử lớn nhất và nhỏ nhất (trimmed mean)
# - Làm tròn đến số chữ số thập phân tùy chọn
# def trimmed_mean(numbers, trim = 0, decimal = 2):
#     sorted_nums = sorted(numbers)
#     if trim > 0:
#         sorted_nums = sorted_nums[trim:-trim]  # Bỏ trim phần tử lớn nhất và nhỏ nhất
#     return round(sum(sorted_nums) / len(sorted_nums),decimal)
# # Ví dụ sử dụng
# data = [10, 20, 30, 40, 50, 60, 70]
# print(trimmed_mean(data, trim=2, decimal=1))  # 40.0 (bỏ 10, 20, 60, 70)    

# Bài 2: *args và **kwargs
# Viết hàm log linh hoạt:
# log("INFO", "Server started")
# log("ERROR", "DB failed", "Retry in 5s", host="db01", port=5432)
# def log(level, *messages, **context):
#     ctx = " | ".join(f"{k}={v}" for k, v in context.items())
#     print(type(messages))
#     for msg in messages:
#         print(f"[{level}] {msg}" + (f" ({ctx})" if ctx else ""))

# log("INFO", "Server started", "List of messages", host="web01", port=8080)

def make_counter(start=0, step=1):
    count = start
    
    def counter():
        nonlocal count
        count += step
        return count
    
    def reset():
        nonlocal count
        count = start
        
    def get():
        return count
    
    return counter, reset, get

counter, reset, get = make_counter(10, 2)
print(counter())  # 12
print(counter())  # 14
print(counter())  # 14
print(reset())    # None
print(get())      # 10