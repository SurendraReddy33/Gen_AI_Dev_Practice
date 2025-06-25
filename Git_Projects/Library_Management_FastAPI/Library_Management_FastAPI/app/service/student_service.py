import json
import os
from app.utils.decorators import handle_exceptions
from app.utils.logger import get_logger

logger = get_logger(__name__)
STUDENT_FILE = "app/data/students.json"

@handle_exceptions
def load_students():
    if not os.path.exists(STUDENT_FILE):
        return []
    with open(STUDENT_FILE, 'r') as f:
        return json.load(f)

@handle_exceptions
def save_students(students):
    with open(STUDENT_FILE, 'w') as f:
        json.dump(students, f, indent=4)
    logger.info("Students data saved")

@handle_exceptions
def add_student(student: dict):
    students = load_students()
    students.append(student)
    save_students(students)
    return {"message": "Student added successfully"}

@handle_exceptions
def update_student(student_id, updates):
    students = load_students()
    updated = False
    for student in students:
        if student.get("student_id") == student_id:
            student.update(updates)
            updated = True
            break
    if updated:
        save_students(students)
        return {"message": "Student updated successfully"}
    return {"message": "Student ID not found"}

@handle_exceptions
def list_students():
    return load_students()

@handle_exceptions
def delete_student(student_id):
    students = load_students()
    updated = [s for s in students if s.get("student_id") != student_id]
    if len(updated) == len(students):
        return {"message": "Student not found"}
    save_students(updated)
    return {"message": "Student deleted successfully"}

@handle_exceptions
def search_student_by_name(name):
    students = load_students()
    results = [s for s in students if name.lower() in s.get("name", "").lower()]
    return results if results else {"message": "No student found with that name"}
