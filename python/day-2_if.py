#Simple If-else
def check_age(age: int) -> str:
    if age >= 18:
        return "Adult"
    else:
        return "minor"

#Multiple conditions using elif
def grade_score(score: int) -> str:
    if score >= 90:
        return "Excellent"
    elif score >=80:
        return "very good"
    elif score >= 50:
        return "not bad"
    else:
        return "fail"

#Nested if statements
def validate_user(age: int,is_registered: bool) -> str:
    if age >= 18:
        if is_registered:
            return "Access granted"
        else:
            return "access denied"
    else:
        return "minor"

simple = check_age(18)
print(simple)

multi_elif = grade_score(9)
print(multi_elif)

nested = validate_user(23,True)
print(nested)