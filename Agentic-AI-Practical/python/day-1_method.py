def welcome():
    print("Hello world")

def get_user_age():
    name=27
    return name

def get_user_age1():
    age=27
    return age

def get_user_information():
    name="Voonna"
    age=26
    return name,age

username,age=get_user_information()
method1=welcome()
method2=get_user_age()
method3=get_user_age1()


print(f"Dear {username} your age is {age}")


def divide(a,b):
    quotient=a/b
    remainder=a%b
    return quotient,remainder

q,r=divide(17,5)
print(f"quotient is {q} and remainder is {r}")