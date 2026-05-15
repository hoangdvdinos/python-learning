# total = 0
# n = 1

# while n < 100:
#     total += n
#     n+=1
# print(f"total = {total}")

secret = 123

# while True:
#     guess = input("Guess the number: ")
#     print(type(guess))
#     if not guess.isdigit():
#         print("Please enter a valid number.")
#         guess = input("Guess the number: ")
#         continue
#     guess = int(guess)
#     if guess == secret:
#         print("You win!")
#         break
#     elif guess < secret:
#         print("Too low, try again.")
#     else:
#         print("Too high, try again.")

# for char in "Python":
#     print(char)
    
# user = {"name": "Hoang", "age": 25, "city": "HCM"}    
# for key, value in user.items():
#     print(f"{key}: {value}")
    
# fruits = ["apple", "banana", "cherry"]
# for i, fruit in enumerate(fruits, start=1):
#     print(f"{i}: {fruit}")

print(type(range(5)))  # <class 'range'>
print(range(5))  # range(0, 5)

fruits = ["apple", "banana", "cherry"]
fruit_lengths = {fruit: len(fruit) for fruit in fruits}
print(fruit_lengths)  # {'apple': 5, 'banana': 6, 'cherry': 6}