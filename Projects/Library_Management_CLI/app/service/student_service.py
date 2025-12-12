import json
import os
from app.utils.decorators import handle_exceptions
from app.utils.logger import get_logger
from app.models.student import Student

logger = get_logger(__name__)
STUDENT_FILE = "app/data/students.json"

@handle_exceptions
def load_students():
    if not os.path.exists(STUDENT_FILE):
        return []
    with open(STUDENT_FILE, 'r') as f:
        students_data = json.load(f)
        return [Student.from_dict(s) for s in students_data]
    
@handle_exceptions
def save_students(students):
    with open(STUDENT_FILE, 'w') as f:
        json.dump([student.to_dict() for student in students], f , indent=4)
    logger.info("Students data saved")

@handle_exceptions
def add_student(student):
    students = load_students()
    students.append(student)
    save_students(students)
    print("Student Added successfully")

@handle_exceptions
def update_student(student_id, updates):
    students = load_students()
    students = [Student.from_dict(s) for s in students]
    updated = False
    for i, stu in enumerate(students):
        if str(stu.student_id) == str(student_id):
            for key, value in updates.items():
                if hasattr(stu, key):
                    setattr(stu, key, value)
            updated = True
            break
    if updated:
        save_students(students)
        print("Student data updated successfully")
    else:
        print("Student ID not Found")    


@handle_exceptions
def list_students():
    students = load_students()
    if not students:
        print("No students added")
        return
    for stu in students:
        print(f"{stu.student_id} - {stu.name} - {stu.department} - {stu.year}")

@handle_exceptions
def delete_students(student_id):
    students = load_students()
    updated = [s for s in students if s.student_id != student_id]
    if len(updated) == len(students):
        print("Student not found")
    else:
        save_students(updated)
        print("student deleted")

@handle_exceptions
def search_student_by_name(name):
    students = load_students()
    found = False
    for stu in students:
        if name.lower() in stu.name.lower():
            print(f"{stu.student_id} - {stu.name} - {stu.department} - {stu.year}")
            found = True
    if not found:
        print("No student found with that name")