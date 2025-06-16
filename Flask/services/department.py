import json
import os

from utils.decorators import log_exception
from utils.helpers import load_from_json, save_to_json, logger
DEPARTMENTS_JSON = os.path.join(os.path.dirname(__file__), "..", "json", "departments.json")

class Department:
    def __init__(self, dept_id, dept_name):
        self.dept_id = dept_id
        self.dept_name = dept_name

    def to_dict(self):
        return vars(self)

    @log_exception
    @classmethod
    def add_department(cls):
        dept_id = input("please enter department id : ")
        dept_name = input("please enter department name : ")

        departments = load_from_json(DEPARTMENTS_JSON)

        department = Department (dept_id, dept_name).to_dict()
        departments.append(department)
        save_to_json(departments, DEPARTMENTS_JSON)

    @log_exception
    def list_departments():
        """LIST ALL SAVED DEPARTMENTS"""
        departments = load_from_json(DEPARTMENTS_JSON)
        logger.info("All departments loaded....")
        print("\033[92m\nAvailable Departments : ]")
        for d in departments:
            print(f"[{d['dept_id']}] {d['dept_name']}")
        print("\033[om")


    def __str__(self):
        return f"Department [{self.dept_id}] - {self.dept_name}"


