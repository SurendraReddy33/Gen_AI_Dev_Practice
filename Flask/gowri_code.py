from flask import Flask,request, jsonify

import json
import os
import logging

app= Flask(__name__) # Create an flask Application

DATA_FILE="users.json"
@app.route("/welcome")
def hello():
    return "Hello Gowri Ganesh"

@app.route("/register",methods=["POST"])
def register_user():
    data = request.get_json()   # get the users supplied data
    #Mandatory fields
    #Take each item from required and compare with each item of body values
    required =["first_name","last_name","email","dob","password"]
    users=load_user()
    if not all(r in data for r in required):
        return jsonify({"Message":"All fields required",
                        "Code":"501"}),400
    # Add new users details for the user collection
    users.append(data)
    # save users details back to the json
    save_user(users)

    return jsonify({"Message":"User Registered successfully",
                    "Code":"200"})

@app.route("/users")
def list_users():
    users=load_user()
    return users




@app.route("/change_password", methods=["POST"])
def change_password():
    data = request.get_json()
    email = data.get("email")
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    user_data=load_user()
    if not all([email,old_password,new_password]):
        return jsonify({"message": "All fields are reqired "}),404
    try:
        for user in user_data:
            if user.get("email")== email and user.get("password") == old_password:
                 user["password"]=new_password
                 save_user(user)
                 return jsonify({
                "Message":"Password Changed Successfully"
            }),200
            return jsonify({"message":" email or password is wrong ",
                            }),401
       
    except Exception as e:
        return ({"Message":"Something wrong please check your credntails"}),505
           
       
       
       
       



#Helper method
#Genrator - next () - it will return first match found if not returns None
@app.route("/find_user/<email>")
def fetch_user(email):
    user=find_user_by_email(email)
    if user:
        return user
    return jsonify({"Message":" User not Found"}),404

def find_user_by_email(email):
    users=load_user()
    return next((u  for u  in users if u["email"]==email),None)


def load_user():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE , "r") as f:
        return json.load(f)
   
def save_user(users):
    with open(DATA_FILE,"w") as f:
        json.dump(users,f)
       
       
       
if __name__=="__main__":
    app.run(debug=True)
