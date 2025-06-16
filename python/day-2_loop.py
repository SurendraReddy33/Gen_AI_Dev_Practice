student={"name":"Amit","age":20,"marks":85}

for key,value in student.items():
    print(key, "=>", value)

for key in student.items():
    print(key)


print(student.get("name"))

print(student.get("blablabla"))

student.clear()

print(student)