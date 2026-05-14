import greet  # <- dòng này sẽ in __name__ của greet.py

print(f"[main.py] __name__ = '{__name__}'")
print()

print("Calling functions from greet module:")
print(greet.greet("Hoang"))
print(greet.farewell("Hoang"))
