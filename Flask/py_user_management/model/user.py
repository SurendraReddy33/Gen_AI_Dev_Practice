
import json
import os


DATA_FILE = "users.json"

class User:
    def __init__(self, first_name, last_name, email, dob, password):
        self.first_name = first_name 
        self.last_name = last_name
        self.email = email 
        self.dob = dob
        self.password = password
    
    # Converting Object => JSON 
    def to_dict (self):
        return {
        "first_name" : self.first_name, 
        "last_name" : self.last_name,
        "email" : self.email ,
        "dob" : self.dob,
        "password" : self.password
        }
    
    # Convert JSON To Object
    @staticmethod
    def from_dict(user_json_data):
        return User (
            user_json_data["first_name"],
            user_json_data["last_name"],
            user_json_data["email"],
            user_json_data["dob"],
            user_json_data["password"],
        )
    

# **** Helper Methods *****
def load_users():
    if not os.path.exists(DATA_FILE):
        return []
    with open (DATA_FILE, "r") as f:
        json_data =  json.load(f)
        return [User.from_dict(u) for u in json_data]

def save_users(users):
    with open (DATA_FILE, "w") as f:
        json.dump ([u.to_dict() for u in users], f, indent=4)

def find_user_by_email(email):
    email = email.strip().lower()
    users = load_users()    
    # Yelid with email address and return the first found, else None
    return next((u for u in users if u.email.strip().lower() == email), None)
