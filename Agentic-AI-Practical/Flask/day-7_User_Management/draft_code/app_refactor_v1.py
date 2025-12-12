from flask import Flask, request, jsonify

import json
import os
import logging

# Create a Flask Application
app = Flask (__name__)

logging.basicConfig(
    filename="app.log",
    level= logging.INFO,
    format= "%(asctime)s [%(levelname)s] %(message)s"
)

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
    

# *****Begin API Route Implementation

@app.route("/register", methods = ["POST"])
def register_user():

    # Get the User supplied values From Body
    data = request.get_json()    
    required = ["first_name", "last_name", "email", "dob", "password"]

    # Add the user supplied values are present in required field?
    if not all(r in data for r in required): 
        return jsonify({"message": "***All Fields are required", "Code": "422"})
    
    # Load the existing  users from JSON File
    users = load_users()

    user = User (
            data["first_name"],
            data["last_name"],
            data["email"],
            data["dob"],
            data["password"])    

    users.append (user) # Add new user detailsl for the users collection    
    save_users (users) # Save users collection back to Storage -> JSON
    return jsonify({"Message":"User Added Succefully", "Code":"200"})

@app.route("/user/login", methods=["POST"] )
def login():
    try:
        # Get the data from Request Post Body
        data = request.get_json()  # Get data from Request Body
        email = data.get("email")
        
        # Load the User Object from email
        user = find_user_by_email(email)
        
        app.logger.info(f"User found is {user}")
        app.logger.info(f"User found is {data.get("email")}")        

        if user and user.password == data.get("password"):
            return jsonify({"message": f"User {email} Logged in"}), 200
        else:
            return jsonify({"message": f"Login failed for user {email}"}), 401
    except Exception as e:
        app.logger.error(f"Internal Server Error {e}")
        return jsonify({"message": f"Internal Server Error {e}"}), 500



# ***** Begin Helper Methods Implementation

# Conver users Object to JSON (Dict)
def load_users():
    if not os.path.exists(DATA_FILE):
        return []
    with open (DATA_FILE, "r") as f:
        json_data =  json.load(f)
        return [User.from_dict(u) for u in json_data]

# Conver users Object to JSON (Dict)
def save_users(users):
    with open (DATA_FILE, "w") as f:
        json.dump ([u.to_dict() for u in users], f, indent=4)

def find_user_by_email(email):
    email = email.strip().lower()
    users = load_users()    
    # Yelid with email address and return the first found, else None
    return next((u for u in users if u.email.strip().lower() == email), None)

if __name__ == "__main__":
    app.run(debug=True, port=5000)