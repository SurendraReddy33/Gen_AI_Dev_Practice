from datetime import datetime
from app.model.project import Project

class Employee:
    def __init__(self,emp_id, name, department, designation, salary, dob, location, projects):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.designation = designation
        self.salary = salary
        self.dob = dob
        self.location = location
        self.projects = [ Project(**p) for p in projects]

    def benched_emps(self):
        return len(self.projects) == 0
    
    def project_status(self, status):
        return any(p.status == status for p in self.projects)
    
    def age(self):
        birth_date = datetime.strptime(self.dob, "%Y-%m-%d")
        return (datetime.now() - birth_date).days // 365
    
    def convert_to_dict(self):
        return {
            "emp_id": self.emp_id,
            "name": self.name,
            "department": self.department,
            "designation": self.designation,
            "salary": self.salary,
            "dob": self.dob,
            "age": self.age(),
            "location": self.location,
            "projects": [p.convert_to_dict() for p in self.projects]

        }