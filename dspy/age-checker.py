import dspy

class AgeChecker(dspy.predict):
    super().__init__(signature="name, age -> message")

    def forward(self, name: str, age:str) -> str:
        age = int(age)
        if age >= 18:
            return f"{name} , you are eligible to vote."
        else:
            return f"{name}, you are not eligible to vote."
        
checker = AgeChecker()
response = checker(name="John", age="20")
print(response)