class Animal:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def speak(self) -> str:
        return f"{self.name} phát ra âm thanh"

    def describe(self) -> str:
        return f"{self.name} ({self.age} tuổi)"

class Dog(Animal):
    def __init__(self, name: str, age: int, breed: str):
        super().__init__(name, age)     # Gọi constructor của parent
        self.breed = breed

    def speak(self) -> str:            # Override phương thức
        return f"{self.name} sủa: Gâu gâu!"

    def fetch(self) -> str:
        return f"{self.name} chạy đi nhặt bóng"

class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} kêu: Meo meo!"

dog = Dog("Rex", 3, "Labrador")
cat = Cat("Whiskers", 5)

print(dog.speak())          # Rex sủa: Gâu gâu!
print(dog.describe())       # Rex (3 tuổi) — kế thừa từ Animal
print(dog.fetch())          # Rex chạy đi nhặt bóng
print(cat.speak())          # Whiskers kêu: Meo meo!

# isinstance kiểm tra chuỗi kế thừa
print(isinstance(dog, Dog))     # True
print(isinstance(dog, Animal))  # True — Dog là Animal
print(isinstance(dog, Cat))     # False