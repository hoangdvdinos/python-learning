# FizzBuzz
# In số 1-30. Chia hết 3 → "Fizz", chia hết 5 → "Buzz", cả hai → "FizzBuzz"
# for i in range(1, 31):
#     if(i % 15 ==0):
#         print("FizzBuzz")
#     elif(i % 3 == 0):
#         print("Fizz")
#     elif(i % 5 == 0):
#         print("Buzz")
#     else:
#         print(i)
        
# Bài 2: Tìm tất cả số nguyên tố từ 2 đến 50
# for nguyen_to in range(2, 51):
#     for i in range(2, nguyen_to):
#         if(nguyen_to % i == 0):
#             break
#     else:
#         print(nguyen_to)
        
# text = "mississippi"
# print(set(text)) # {'i', 's', 'p', 'm'} - tập hợp các ký tự trong chuỗi, không có thứ tự và không trùng lặp
# dict_count = {char: text.count(char) for char in set(text)}

# fibonaci
# a = 0
# b = 1
# fib_sum = 0
# while a < 100:
#     fib_sum = a
#     a,b = b, a + b
# print(f"fib_sum: {fib_sum}")

# ma tran bang cuu chuong
# for i in range(1, 10):
#     for j in range(1, 10):
#         print(f"{i} * {j} = {i*j}", end="\t")

# table = {(i, j): i * j for i in range(1, 10) for j in range(1, 10)}
# # print(table, end="\t")
# for values, result in table.items():
#     print(f"{values[0]} * {values[1]} = {result}", end="\t")

# bubble sort
# arr = [5, 2, 9, 1, 5, 6]
# n = len(arr)
# for i in range(n):
#     for j in range(0, n - i - 1):
#         if arr[j] < arr[j + 1]:
#             arr[j], arr[j + 1] = arr[j + 1], arr[j]
# print("Sorted array is:", arr)

# selection sort
# arr = [64, 25, 12, 22, 11]
# n = len(arr)
# for i in range(n):
#     min_idx = i
#     for j in range(i + 1, n):
#         if arr[j] < arr[min_idx]:
#             min_idx = j
#         arr[i], arr[min_idx] = arr[min_idx], arr[i]
# print("Sorted array is:", arr)

# insertion sort
arr = [12, 11, 13, 5, 6]
n = len(arr)
for i in range(1, n):
    key = arr[i]
    j = i - 1
    while j >= 0 and key < arr[j]:
        arr[j + 1] = arr[j]
        j -= 1
    arr[j + 1] = key
print("Sorted array is:", arr)