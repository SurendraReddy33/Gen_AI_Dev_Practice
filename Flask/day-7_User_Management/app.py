from flask import Flask, request, jsonify
from model.user import User
from model.user_helper import UserHelper

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
    for u in users:
        user_data=User.to_dict(u)
        if data["email"]== user_data["email"]:
            app.logger.info(f"Already user exists: {user_data['email']}")
            return jsonify({"message" : "Already exists" })


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


@app.route("/users", methods=["GET"])
def list_all_users():
    users = load_users()
    user=[]
    # user_data= [ user.to_dict() for user in users]
    for u in users:
        user.append(User.to_dict(u))
   
    return jsonify(user)



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



@app.route("/get_user/<email>",methods=["GET"])
def get_user(email):
    user=find_user_by_email(email)
    if user:
        return jsonify(user.to_dict()),200
    else:
        return jsonify({"message":"User Doesn't Exist"}),404


@app.route("/user/change_password", methods = ["POST"])
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
        print(users)
        for u in users:
            print(u.email)
            stored_email = u.email.strip().lower()
            app.logger.info(f"Comparing emails: input='{email}' stored='{stored_email}'")
           
            if stored_email == email:
                app.logger.info("Email match found")
                if u.password == old_password:
                    u.password= new_password
                    save_users(users)
                    return jsonify({"message": "Password changed successfully."}), 200
                else:
                    return jsonify({"message": "Old password is incorrect."}), 400
 
        app.logger.info(f"No user found with email: {email}")
        return jsonify({"message": "User does not exist."}), 404
    except Exception as e:
        app.logger.error(f"Error in change_password: {str(e)}")
        return jsonify({"message": f"Something went wrong... {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)