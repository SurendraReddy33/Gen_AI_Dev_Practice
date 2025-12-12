
from datetime import datetime
from app.model.project import Project

class Employee:
    """Represents an employee in the organization.
    
    This class stores employee information including personal details,
    job-related information, and associated projects. It also provides
    methods to query the employee's status and project involvement.
    """
    def __init__(self, emp_id, name, department, salary, designation, location, dob, projects):
        """Initialize an Employee object with the provided attributes.
        
        Args:
            emp_id (str): Unique employee identifier
            name (str): Employee's full name
            department (str): Department the employee belongs to
            salary (float): Employee's salary
            designation (str): Employee's job title/designation
            location (str): Employee's work location
            dob (str): Date of birth in 'YYYY-MM-DD' format
            projects (list): List of projects the employee is assigned to
        """
        self.emp_id =  emp_id
        self.name = name 
        self.department = department
        self.salary = salary
        self.designation =  designation
        self.location = location
        self.dob = dob
        self.projects = [ Project(**p) for p in projects]

    def is_on_bench(self):
        """Check if the employee is on bench (not assigned to any projects).
        
        Returns:
            bool: True if employee has no assigned projects, False otherwise
        """
        return len(self.projects) == 0 

    def has_project_with_status(self, status):
        """Check if the employee has any projects with the specified status.
        
        Args:
            status (str): The project status to check for (e.g., 'active', 'completed')
            
        Returns:
            bool: True if employee has at least one project with the given status
        """
        return any(p.status == status for p in self.projects)
    
    def get_age(self):
        """Calculate the employee's age based on their date of birth.
        
        Returns:
            int: Employee's age in years
        """
        birth_date = datetime.strptime(self.dob, "%Y-%m-%d")
        return (datetime.now() - birth_date).days // 365
    
    def to_dict(self):
        """Convert the Employee object to a dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the employee with all attributes
                  and calculated fields like age and serialized projects
        """
        return {
            "emp_id": self.emp_id,
            "name": self.name,
            "department": self.department,
            "salary": self.salary,
            "designation": self.designation,
            "location": self.location,
            "dob": self.dob,
            "age": self.get_age(),  # Include calculated age field
            "projects": [p.to_dict() for p in self.projects]  # Serialize nested projects
        }