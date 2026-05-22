# with open("test1.txt", "a") as f:
#     f.write("Hello, World!")

# with open("test1.txt", "r") as f:
#     content = f.read()
#     print(content)
    
with open("test1.txt", "r") as f:
    content = f.readlines()
    print(content)
