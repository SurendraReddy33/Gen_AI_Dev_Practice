import json
import os
from datetime import datetime
from app.utils.decorators import handle_exceptions
from app.utils.logger import get_logger
from app.service.book_service import load_books, save_books
from app.service.student_service import load_students

logger = get_logger(__name__)
ISSUE_FILE = "app/data/issued.json"

@handle_exceptions
def load_issued():
    if not os.path.exists(ISSUE_FILE):
        return []
    with open(ISSUE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

@handle_exceptions
def save_issued(data):
    with open(ISSUE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    logger.info("Issued records saved")

@handle_exceptions
def issue_book(student_id, book_id):
    students = load_students()
    books = load_books()
    if not any(s["student_id"] == student_id for s in students):
        return {"message": "Student ID not found"}
    if not any(b["book_id"] == book_id and b["available"] for b in books):
        return {"message": "Book not available"}

    issued = load_issued()
    issued.append({
        "student_id": student_id,
        "book_id": book_id,
        "issue_date": datetime.now().strftime("%Y-%m-%d"),
        "return_date": None
    })
    for book in books:
        if book["book_id"] == book_id:
            book["available"] = False
    save_issued(issued)
    save_books(books)
    return {"message": "Book issued successfully"}

@handle_exceptions
def return_book(student_id, book_id):
    issued = load_issued()
    books = load_books()
    returned = False
    for record in issued:
        if record["student_id"] == student_id and record["book_id"] == book_id and not record["return_date"]:
            record["return_date"] = datetime.now().strftime("%Y-%m-%d")
            returned = True
            break
    if not returned:
        return {"message": "Issued record not found"}

    for book in books:
        if book["book_id"] == book_id:
            book["available"] = True
            break

    save_issued(issued)
    save_books(books)
    return {"message": "Book returned successfully"}

@handle_exceptions
def list_record_books():
    return load_issued()
