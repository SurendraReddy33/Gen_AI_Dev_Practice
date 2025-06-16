def login_user():
    max_attempts = 3
    attempts = 0
    correct_password = "admin"

    while attempts < max_attempts:
        password = input("please enter your password : ")
        if password == correct_password:
            print("your password is correct")
            return True
        else:
            attempts += 1
            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"warning incorrect password please try again your remaining attempts are {remaining}")
            else:
                print(f"ypur account is locked... too many attempts remaining attempts {remaining}")
    return False

result = login_user()
print(result)
    