import json

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def to_dict(self):
        return {"name": self.name, "age": self.age}

    def save_to_file(self, filename):
        with open(filename,'w') as f:
            json.dump(self.to_dict(),f)

    @classmethod
    def load_from_files(cls,filename):
        with open (filename, 'r') as f:
            data = json.load(f)
        return cls(data['name'],data['age'])

user1 = User("ameet", 50)
user1.save_to_file("ameet.json")

user2 = User.load_from_files('ameet.json')
print(f"loaded user with name: {user2.name} and age {user2.age}")

