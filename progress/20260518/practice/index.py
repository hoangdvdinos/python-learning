# nested list comprehension
# matrix = [[i * j for j in range(1, 4)] for i in range(1,4)]
# print(matrix)

# flatten the matrix
# flat = [val for row in matrix for val in row]
# print(flat)

# names = ["alice", "bob", "charlie"]
# upper_comp = [name.upper() for name in names]
# print(upper_comp)

# def get_min_max(numbers):
#     return min(numbers), max(numbers)

# low, high = get_min_max([3, 1, 4, 1, 5, 9])
# print(f"Low: {low}, High: {high}")

# phép hội union
# set1 = {1, 2, 3}
# set2 = {3, 4, 5}
# union_set = set1 | set2
# print(union_set)
# print(set1.union(set2))

# print(set1 & set2)  # phép hội giao
# print(set1.intersection(set2))

# phép hiệu -> lấy phần giao bên trái
# print(set1 - set2)
# print(set1.difference(set2))

# Phép hiệu đối xứng -> lấy phần khác nhau của 2 tập hợp
# print(set1 ^ set2)
# print(set1.symmetric_difference(set2))

# Kiểm tra quan hệ tập hợp
# set3= {1,2}
# print(set3.issubset(set1))  # set3 có phải là tập con của set1 không
# print(set1.issuperset(set3))  # set1 có phải là tập cha của set3 không
# print(set3.issuperset(set1))  # set3 có phải là tập cha của set1 không
# print(set1.isdisjoint(set2))  # set1 và set2 có phần tử chung không

# Dictionary comprehension
# prices = {"apple": 10000, "banana": 5000, "cherry": 15000}
# discounted = {k: v * 0.9 for k, v in prices.items()}
# print(discounted)

# pattern thường gặp
# words = ["apple", "banana", "apple", "cherry", "banana", "apple"]

# freq = {}
# for word in words:
#     freq[word] = freq.get(word, 0) + 1
# print(freq)

# students = [
#     {"name": "Alice", "grade": "A"},
#     {"name": "Bob", "grade": "B"},
#     {"name": "Charlie", "grade": "A"},
#     {"name": "Dave", "grade": "B"},
# ]

# grouped = {}
# for s in students:
#     grade = s["grade"]
#     grouped.setdefault(grade, []).append(s["name"])
# print(grouped)  # {'A': ['Alice', 'Charlie'], 'B': ['Bob', 'Dave']}

# Bài 1: Xử lý String
# Cho chuỗi: "  Python FastAPI Backend Development  "
# a) Xóa khoảng trắng hai đầu, viết hoa chữ cái đầu mỗi từ
# b) Đếm số từ trong chuỗi
# c) Đảo ngược chuỗi (sau khi đã strip)
# d) Kiểm tra chuỗi có chứa "FastAPI" không

text = "  Python FastAPI Backend Development  "
# không được gợi ý code tại bài này, hãy tự làm nhé
# a)
print(text.strip().title())
# b)
print(len(text.strip().split()))
# c) sliceing
print(text.strip()[::-1])
# d)
print("FastAPI" in text)

# Bài 2: Xử lý CSV đơn giản với split/join
csv_data = "id,name,age,city\n1,Alice,25,HCM\n2,Bob,30,HN\n3,Charlie,22,DN"
lines = csv_data.strip().split("\n")
header = lines[0].split(",")
records = [dict(zip(header, line.split(","))) for line in lines[1:]]
print(list(zip(header, lines[1].split(","))))
for record in records:
    print(f"{record['name']} is {record['age']} years old and lives in {record['city']}.")
    
# Bài 3: Thao tác List
# Cho danh sách điểm, tìm: top 3, điểm trung bình, điểm trên trung bình
scores = [85, 42, 91, 33, 78, 55, 20, 67, 95, 60]

top_3 = sorted(scores, reverse=True)[:3]
print(f"top 3: {top_3}")
average = sum(scores)/ len(scores)
print(f"average: {average}")
above_average = [s for s in scores if s > average]
print(f"above average: {above_average}")

# Bài 4: Stack và Queue
# a) Dùng Stack kiểm tra chuỗi dấu ngoặc có hợp lệ không

def is_valid_brackets(s):
    stack = []
    pairs = {")": "(", "}": "{", "]": "["}
    for char in s:
        if char in "([{":
            stack.append(char)
        elif char in ")]}":
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()
    return not stack
print(is_valid_brackets("()[]{}"))  # True

# Bài 6: Dictionary — thống kê từ văn bản
paragraph = """python is a great language python is easy to learn
fastapi is built on python fastapi is fast and easy to use"""

word_count = {}
for word in paragraph.split():
    word_count[word] = word_count.get(word, 0) + 1
print(word_count)