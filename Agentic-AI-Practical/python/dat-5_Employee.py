# Build a Employee and Department Management system
# Employee
# >> Add Employee
# >> Delete Employee
# >> List Employee
# >> List Employee By Criteria - 
# >> Find Employee with Highest Salary
# >> Find Employee with Lowest Salary

# Department
# >> Add Department
# >> List Department
# >> Delete Department

# Roles
# Roles => Software Developer
# Roles => IT - Manager
# Roles => Hr - Manager

# JSON
# employee.json
# department.json
# role.json

import json
import os


#File Path
EMPLOYEES_JSON = "employees.json"
DEPARTMENTS_JSON = "departments.json"
ROLES_JSON = "roles.json"


def save_to_json(data, file):
    """save a list of dictionaries to a JSON file"""
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)


def load_from_json(file):
    """Load and return a list of dictionaries from a JSON file"""
    if not os.path.exists(file):
        return []
    with open(file, 'r') as f:
        return json.load(f)

# Implmementation classes
class Employee:
    def __init__(self, emp_id, first_name, last_name, doj, salary, department, role):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.doj = doj
        self.salary = salary
        self.department = department
        self.role = role

    def to_dict(self):
        return vars(self)

    def __str__(self):
        return f"Employee [{self.emp_id}] - {self.first_name} - {self.last_name}"

    @classmethod
    def add_employee(cls):
        emp_id = input("Enter the employee id : ")
        first_name = input("Enter the employee first name : ")
        last_name = input("Enter the employee last name : ")
        doj = input("Enter the employee date of birth : ")
        salary = input("Enter the employee salary : ")
        department = input("Enter the employee department : ")
        role = input("Enter the employee role : ")

        # LOAD THE EXISTING EMPLOYEE LIST
        employees = load_from_json(EMPLOYEES_JSON)
        emp = Employee(emp_id, first_name, last_name, doj, salary, department, role).to_dict()
        employees.append(emp) # appended the new employee into the existing list
        save_to_json(employees, EMPLOYEES_JSON) # recreate json file
        print("employee is added to the collection : ")

    def list_employees():
        """LIST ALL SAVED employees"""
        employees = load_from_json(EMPLOYEES_JSON)
        print("\033[92m\nRegistered Employees : ")
        for e in employees:
            print(f"[{e['first_name']}] : {e['last_name']} : {e['salary']}")
        print("\033[om")

    def delete_employee():
        emp_id = input("Enter the Employee ID to delete : ")
        employees = load_from_json(EMPLOYEES_JSON)
        new_list = list(filter(lambda e: e['emp_id'] != emp_id, employees))
        save_to_json(new_list, EMPLOYEES_JSON) #RECREATE THE EMPLOYEE JSON
        print("Employee is deleted from the collection : ")

    

class Department:
    def __init__(self, dept_id, dept_name):
        self.dept_id = dept_id
        self.dept_name = dept_name

    def to_dict(self):
        return vars(self)

    @classmethod
    def add_department(cls):
        dept_id = input("please enter department id : ")
        dept_name = input("please enter department name : ")

        departments = load_from_json(DEPARTMENTS_JSON)

        department = Department (dept_id, dept_name).to_dict()
        departments.append(department)
        save_to_json(departments, DEPARTMENTS_JSON)

    def list_departments():
        """LIST ALL SAVED DEPARTMENTS"""
        departments = load_from_json(DEPARTMENTS_JSON)
        print("\033[92m\nAvailable Departments : ]")
        for d in departments:
            print(f"[{d['dept_id']}] {d['dept_name']}")
        print("\033[om")


    def __str__(self):
        return f"Department [{self.dept_id}] - {self.dept_name}"



class Role:
    def __init__(self, role_id, role_name):
        self.role_id = role_id
        self.role_name = role_name

    def to_dict(self):
        return vars(self)

    def __str__(self):
        return f"Role [{self.role_id}] - {self.role_name}"


    @classmethod
    def add_role(cls):
        role_id = input("please enter role id : ")
        role_name = input("please enter role name : ")

        roles = load_from_json(ROLES_JSON)
        role = Role(role_id, role_name).to_dict()
        roles.append(role)
        save_to_json(roles, ROLES_JSON)

    def list_roles():
        """LIST ALL SAVED ROLES"""
        roles = load_from_json(ROLES_JSON)
        print("\033[92m\nAvailable Roles : ]")
        for r in roles:
            print(f"[{r['role_id']}] {r['role_name']}")
        print("\033[om")


def menu():
    while True:
        print("\n --------EMPLOYEE SYSTEM---------")
        print("1. Add Department")
        print("2. List Departments")
        print("3. Add Roles")
        print("4. List Roles")
        print("5. Add Employee")
        print("6. List Employees")
        print("7. Delete Employee")
        print("0. Exit")

        choice = input("Enter your choice : ")

        if choice == "1":
            Department.add_department()
        elif choice == "2":
            Department.list_departments()
        elif choice == "3":
            Role.add_role()
        elif choice == "4":
            Role.list_roles()
        elif choice == "5":
            Employee.add_employee()
        elif choice == "6":
            Employee.list_employees()
        elif choice == "7":
            Employee.delete_employee()
        elif choice == "0":
            print("\033[92mExiting... Bye\033[0m")
        else:
            print("\033[91mInvalid choice\033[0m")

            
if __name__ == "__main__":
    menu()