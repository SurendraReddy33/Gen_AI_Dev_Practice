def add_two_numbers(first_number:int, second_number:int) -> int:
    return first_number + second_number

def greet_user(name: str = "guest") -> str:
    return f"Hello {name}"

result= greet_user()
print(result)

addition = add_two_numbers(23,4)
print(addition)