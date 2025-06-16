import json
import os

from utils.decorators import log_exception
from utils.helpers import load_from_json, save_to_json, logger
EMPLOYEES_JSON = os.path.join(os.path.dirname(__file__), "..", "json", "employees.json")

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

    @log_exception
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

    @log_exception
    def list_employees():
        """LIST ALL SAVED employees"""
        employees = load_from_json(EMPLOYEES_JSON)
        logger.info(f"All Employees loaded....")
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