# Bài 1: Tính tiền sau thuế
price = 250_000
tax_rate = 0.1
total = price + price * tax_rate
print(f"Giá gốc: {price:,} VND")
print(f"Thuế: {price * tax_rate:,.0f} VND")
print(f"Tổng: {total:,.0f} VND")

year = 2024
is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
print(f"{year} {'là' if is_leap else 'không phải'} năm nhuận")

score = 85
grade = "A" if score >= 90 else "B" if 80 <= score < 90 else "C" if 70 <= score < 80 else "F"
print(f"Điểm {score} → Xếp loại {grade}")

score = 8
grade = "A" if score > 9 else "B" if score <=9 else "C" if score <=8 else "F"
print(f"Điểm {score} → Xếp loại {grade}")