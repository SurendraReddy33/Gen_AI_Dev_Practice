
# dict
person = {"name": "Ameyaan", "age": 50}

def greet(name, age):
    print (f"Hello {name}, You are {age} old ")

# greet ("Ameyaan", 50)
#greet (person["name"],person["age"] )
#greet (name=person["name"], age = person["age"])
greet (**person) # Will uppack -> **kwargs -> **person = "name=Ameyaan", "age=50"
