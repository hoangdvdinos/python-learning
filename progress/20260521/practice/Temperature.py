class Temperature:
    def __init__(self, celsius):
        self.value = celsius
    
    @property
    def celsius(self) -> float:
        return self.value
    
    @celsius.setter
    def celsius(self, value: float):
        self.value = value
    
    @property
    def fahrenheit(self) -> float:
        return self.value * 9 / 5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value: float):
        self.value = (value - 32) * 5 / 9
        
if __name__ == "__main__":
    temp = Temperature(25)
    print(temp.celsius)      # 25
    print(temp.fahrenheit)   # 77.0
    
    temp.fahrenheit = 86
    print(temp.celsius)      # 30.0
    print(temp.fahrenheit)   # 86.0