class Student:
    def __init__(self, student_id, name, department, year):
        self.student_id = student_id
        self.name = name
        self.department = department
        self.year = year

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "department": self.department,
            "year": self.year,
        }
    
    @classmethod
    def from_dict(cls, data):
        if isinstance(data, dict):
            return cls(
                student_id= data.get("student_id"),
                name = data.get("name"),
                department = data.get("department"),
                year = data.get("year")
            )
        elif isinstance(data, Student):
            return data
        
    
