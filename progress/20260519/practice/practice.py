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

data = range(1, 1000001)
filtered = (n for n in data if n % 2 == 0)     # Chỉ số chẵn
squared  = (n ** 2 for n in filtered)           # Bình phương
result   = sum(n for n in squared if n < 1000) 
print(result)