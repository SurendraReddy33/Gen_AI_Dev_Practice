#dict
#key=> "always string"
#value => int,float, string, dict
employee_records = {
    "Amit": {
        "employee_id":101,
        "department": {
            "id":1,
            "name":"IT"
        },
        "Salary": {
            "basic": 40000,
            "bonus": 5000,
            "total": 45000
        }
    },
    "Sara" : {
        "employee_id":102,
        "department": {
            "id": 2,
            "name": "HR"
        },
        "salary": {
            "basic": 35000,
            "bonus": 4000,
            "total": 39000
        }
    }
}

print(employee_records["Amit"]["Salary"]["total"])
print(employee_records["Sara"]["department"]["id"])

#get("salary")  => None
#get("salary", "Not available") => Not available

total_salary = employee_records.get("blablabla",{}).get("salary",{}).get("total","Not available")
print(total_salary)