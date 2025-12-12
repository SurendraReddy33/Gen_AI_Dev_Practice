#List
student_list = ["Ishaan","Ameet","Vijay"]

#dict => Key:Value
student_marks = { "Ameet":70, "Ishaan":90, "Vijay":97, "Ameet":100}

print(student_list)
print(student_marks)


country_codes = {"India":"IN", "USA": "US", "Japan": "JP"}
print(country_codes)

#key : value -> Int, str, dict, list
employee_details = {
    "Shravanee" : {"employee_id" : 1, "department":{
        "name": "HR", "id": 321,"salary":12000
    }},
    "Vonna" : {"employee_id":2, "department":"IT"},
    "Surendra": {"employee_id":3, "department":"IT"},
    "Vijay" : {"employee_id":4, "department":"admin"},
    "vijay": {"employee_id":4, "department":"admin"}
}

print(employee_details)

student = {"name": "Amit", "age": 20, "marks": 85}
print(student)

print(student["name"])
print(student["age"])
print(student["marks"])

#add key to the dict
student["city"]= "Hyderabad"

print(student)
print(student["city"])

#update the key -> value
student["marks"]=20

print(student)

#delete
del student["marks"]
print(student)

#check if key exists or not
print("age" in student)

#get all keys
print(student.keys())

#get all values
print(student.values())



