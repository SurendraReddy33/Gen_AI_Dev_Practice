from flask import Flask, request, jsonify
from model.user import User,find_user_by_email, load_users, save_users

import json
import os
import logging

# Create a Flask Application
app = Flask (__name__)

logs_dir = "logs"
os.makedirs(logs_dir, exist_ok=True)
log_file_path = os.path.join(logs_dir, "app.log")

logging.basicConfig(
    filename=log_file_path,
    level= logging.DEBUG,
    format="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d %(funcName)s()] %(message)s"

    # format= "%(asctime)s [%(levelname)s] %(message)s"
)

# API Route Implementation

@app.route("/register", methods = ["POST"])
def register_user():
    """ register_user : Method will Register a New User in Database """
    
    # Step  1 - Get the User supplied values From Body
    data = request.get_json()    
    required = ["first_name", "last_name", "email", "dob", "password"]

    # Step 2 - Add the user supplied values are present in required field?
    if not all(r in data for r in required): 
        return jsonify({"message": "***All Fields are required", "Code": "422"})
    
    # Step 3 - Load the existing  users from JSON File
    users = load_users()

    # Step 4 - Build User Object from User's Data from Request Body
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
    """ login : Method will check email and password """
    
    try:
        # Get the data from Request Post Body
        data = request.get_json()  # Get data from Request Body
        email = data.get("email")
        
        # Load the User Object from email
        user = find_user_by_email(email)

        if user and user.password == data.get("password"):
            app.logger.info(f"User found is {user} and cred matched")    
            return jsonify({"message": f"User {email} Logged in"}), 200
        else:
            app.logger.info(f"User found is {user} but cred are not matching")
            return jsonify({"message": f"Login failed for user {email}"}), 401
    except Exception as e:
        app.logger.error(f"Internal Server Error {e}")
        return jsonify({"message": f"Internal Server Error {e}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)