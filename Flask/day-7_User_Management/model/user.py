
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
    

