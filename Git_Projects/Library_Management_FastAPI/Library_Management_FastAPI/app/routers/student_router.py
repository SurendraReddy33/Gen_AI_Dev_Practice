from fastapi import APIRouter
from app.service.student_service import (
    add_student, update_student, list_students,
    delete_student, search_student_by_name
)
from app.models.student import Student

router = APIRouter()

@router.post("/students/add")
def create_student(student: Student):
    return add_student(student.dict())

@router.put("/students/{student_id}")
def modify_student(student_id: str, updates: dict):
    return update_student(student_id, updates)

@router.get("/students")
def get_all_students():
    return list_students()

@router.delete("/students/{student_id}")
def remove_student(student_id: str):
    return delete_student(student_id)

@router.get("/students/search/")
def search_student(name: str):
    return search_student_by_name(name)
