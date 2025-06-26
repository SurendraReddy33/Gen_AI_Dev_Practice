from fastapi import APIRouter
from app.service.issue_service import (
    issue_book, return_book, list_record_books
)

router = APIRouter()

@router.post("/issued_books/{student_id}/{book_id}")
def issue(student_id: str, book_id: str):
    return issue_book(student_id, book_id)

@router.post("/return/{student_id}/{book_id}")
def return_issued(student_id: str, book_id: str):
    return return_book(student_id, book_id)

@router.get("/list_issued")
def get_issued_books():
    return list_record_books()
