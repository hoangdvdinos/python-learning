def greet(name):
    return f"Hello, {name}!"

def farewell(name):
    return f"Goodbye, {name}!"

print(f"[greet.py] __name__ = '{__name__}'")

if __name__ == "__main__":
    print("Running directly -> calling functions:")
    print(greet("Hoang"))
    print(farewell("Hoang"))
