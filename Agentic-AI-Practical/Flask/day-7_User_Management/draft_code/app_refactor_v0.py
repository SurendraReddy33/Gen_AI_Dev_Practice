from flask import Flask, request, jsonify

import json
import os
import logging # Framework which allows to Log the Information in file
               # Information - Message, Error  Message, Warning , Dignostic 

app = Flask (__name__) # Create a Flask Application

logging.basicConfig(
    filename="app.log",
    level= logging.INFO,
    format= "%(asctime)s [%(levelname)s] %(message)s"
)

DATA_FILE = "users.json"

@app.route("/")
def hello():
    return "Welcome to User Management Service. You are at Landing Page of API"

@app.route("/register", methods = ["POST"])
def register_user():
    data = request.get_json() # Get the User supplied values From Body
    
    required = ["first_name", "last_name", "email", "dob", "password"]

    permitted = ["first_name", "last_name", "email", "dob", "password", "address"]
    
    # 1. List of Mandatory Fields
    # 2. List of Fields passed by user - via api
    # Take Each item from mandatory (required)  and comare with each item of Body values   
    # x = a + b


    if not all(r in data for r in required): # Add the user supplied values are present in required field?
        return jsonify({"message": "***All Fields are required", "Code": "422"})

    # Todo : Add logic to implement permitted fileds.
    
    users = load_users() # Load the existing  users from JSON File    
    
    # Missing Input Schema Validation
    users.append (data) # Add new user detailsl for the users collection    
    save_users (users) # Save users collection back to Storage -> JSON
    return jsonify({"Message":"User Added Succefully", "Code":"200"})

@app.route("/users", methods=["GET"])
def list_all_users():
    users = load_users()
    return users

# def get_by_email_id(email):
#     return 1



# @app.route("/find_user", methods=["GET"])
# @app.route("/user_details", methods=["GET"])
# @app.route("/userdetails", methods=["GET"])
# @app.route("/user", methods=["GET"])
# @app.route("/email", methods=["GET"])
@app.route ("/user/<email>", methods=["GET"])
def get_user(email):
    user =  find_user_by_email(email)
    if user:
        return jsonify(user),200 # return the user
    
    return jsonify({"error": "User not found"}), 404

@app.route("/user/change_password", methods=["POST"])
def change_password():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No JSON data provided"}), 400
            
        email = data.get("email")
        if not email:
            return jsonify({"message": "Email is required"}), 400
            
        email = email.strip().lower()
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        
        if not old_password or not new_password:
            return jsonify({"message": "Both old_password and new_password are required"}), 400

        users = load_users()
        for u in users:
            stored_email = u["email"].strip().lower()
            app.logger.info(f"Comparing emails: input='{email}' stored='{stored_email}'")
            
            if stored_email == email:
                app.logger.info("Email match found")
                if u["password"] == old_password:
                    u["password"] = new_password
                    save_users(users)
                    return jsonify({"message": "Password changed successfully."}), 200
                else:
                    return jsonify({"message": "Old password is incorrect."}), 400

        app.logger.info(f"No user found with email: {email}")
        return jsonify({"message": "User does not exist."}), 404
    except Exception as e:
        app.logger.error(f"Error in change_password: {str(e)}")
        return jsonify({"message": f"Something went wrong... {str(e)}"}), 500

@app.route("/user/login", methods=["POST"] )
def login():
    try:
        # Get the data from Request Post Body
        data = request.get_json() 
        email = data.get("email")
        user = find_user_by_email(email)

        
        app.logger.info(f"User found is {user}")
        app.logger.info(f"User found is {data.get("email")}")
        

        if user and user["password"] == data.get("password"):
            return jsonify({"message": f"User {email} Logged in"}), 200
        else:
            return jsonify({"message": f"Login failed for user {email}"}), 401
    except Exception as e:
        app.logger.error(f"Internal Server Error {e}")
        return jsonify({"message": f"Internal Server Error {e}"}), 500
    


# Helper Method
# next () - Generator - Returns the first match found

def find_user_by_email(email):
    email = email.strip().lower()
    users = load_users() # Total  = 2

    print (f"Found Users are {users} ")

    # print (f"stored email address is {u["email"]}")

    #u["email"] == email
    
    # Yelid with email address and return the first found, else None
    return next((u for u in users if u["email"].strip().lower() == email), None)


# Storage - JSON Storage
def load_users():
    if not os.path.exists(DATA_FILE):
        return []
    with open (DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open (DATA_FILE, "w") as f:
        json.dump (users, f)


if __name__ == "__main__":
    app.run(debug=True, port=5000)