class User:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def show_user_info(self):
        print(f"Name: {self.name} age: {self.age}")

    @classmethod
    def from_string(cls, data_string):
        name,age = data_string.split("-")
        return cls(name.strip(),int(age))

    @staticmethod
    def is_valid_age(age):
        return 0 < age < 120

#class instance creation = its object of class :user1
user1 = User("ameet","50")
user1.show_user_info()

#class instance creation - using class method
data_string= "ameyaan - 100"
user2 = User.from_string(data_string)
user2.show_user_info()

print(User.is_valid_age(100))
print(User.is_valid_age(190))