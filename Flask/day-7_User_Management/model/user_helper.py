import json
import os
from model.user import User

DATA_FILE = "users.json"


class UserHelper:

    @staticmethod
    # **** Helper Methods *****
    def load_users():
        if not os.path.exists(UserHelper.DATA_FILE):
            return []
        with open (UserHelper.DATA_FILE, "r") as f:
            json_data =  json.load(f)
            return [User.from_dict(u) for u in json_data]

    @staticmethod
    def save_users(users):
        with open (UserHelper.DATA_FILE, "w") as f:
            json.dump ([u.to_dict() for u in users], f, indent=4)

    @staticmethod
    def find_user_by_email(email):
        email = email.strip().lower()
        users = UserHelper.load_users()    
        # Yelid with email address and return the first found, else None
        return next((u for u in users if u.email.strip().lower() == email), None)