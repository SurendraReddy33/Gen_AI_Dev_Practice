#Class variable = class variables are shared across all instances and belong to the class itself, theyre defined outside any method.

#Instance variables = Instance variables (accessed via self) are unique to each object and are typically set in __init__.

class Person:
    def __init__(self,name):
        self.name = name
        self.data = {}
        print(self.name)
        
    def __str__(self):
        return f"Hello i am {self.name}"

    def __repr__(self):
        return f"Person(name='{self.name}')"

    def __len__(self):
        return len(self.data)

    def __getitem__(self,key):
        return self.data.get(key,None)

    def __setitem__(self,key,value):
        self.data[key] =value

    def __call__(self):
        print(f"{self.name} was called like a function")

    def __enter__(self):
        print("entering into context or scope")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exiting from the context or scope")

    def __eq__(self, other): #__eq__ ==> ==
        return isinstance(other, Person) and self.name == other.name

    def __del__(self):
        print(f"{self.name} class is being destroyed")

if __name__ == "__main":
    obj = Person("Ameet")
    print(str(obj))

    print(repr(obj))

    #object{"key"} = value
    obj["skill"]= "Python" #set

    print(obj["skill"]) #get

    print(len(obj)) #len ---->get

    obj()

    with obj:
        print("Hello iam in the block or context")

    print(obj == Person("Ameet"))

    del obj

person1 = Person("Ameet") #object 1

person2 = Person("Ishaan") #Object 2

print(str(Person(name="Ameet")))


