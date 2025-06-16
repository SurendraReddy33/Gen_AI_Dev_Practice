import json
import os
from datetime import datetime
from app.models.issued_record import IssueRecord
from app.service.book_service import load_books
from app.utils.decorators import handle_exceptions
from app.utils.logger import get_logger
from app.service.student_service import load_students

logger = get_logger(__name__)
ISSUE_FILE = "app/data/issued.json"

@handle_exceptions
def load_issued():
    if not os.path.exists(ISSUE_FILE):
        return []
    with open(ISSUE_FILE, "r") as f:
        try:
            data = json.load(f)
            return data if data is not None else []
        except json.JSONDecodeError:
            return []

@handle_exceptions
def save_issued(data):
    with open(ISSUE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    logger.info("saved issued records")

@handle_exceptions
def issue_book(student_id, book_id):
    issued = load_issued()
    students = load_students()
    books = load_books()
    if student_id in students and book_id in books:
        print("if block executed") 
        issued.append({"student_id": student_id , "book_id": book_id, "issue_date":datetime.now().strftime("%Y:%m:%d"), "return_date": None})
    save_issued(issued)
    print("Book issued")
    

@handle_exceptions
def return_book(student_id, book_id):
    issued = load_issued()
    updated = False
    for rec in issued:
        if (rec["student_id"] == student_id and rec["book_id"] == book_id):
            updated = True
            break
    return_list = []
    for rec in issued:
        if updated:
            if (rec["student_id"] != student_id and rec["book_id"] != book_id):
                return_list.append(rec)
        else:
            print("No issued record found")
    logger.info("Successfully returned")
    save_issued(return_list)
    print("Book Returned Successfully")

@handle_exceptions
def list_record_books():
    issued = load_issued()
    if not issued:
        print("No Books issued")
    else:
        for rec in issued:
            print(f"Student ID: {rec['student_id']} | Book ID: {rec['book_id']} | Issued: {rec['issue_date']}")
