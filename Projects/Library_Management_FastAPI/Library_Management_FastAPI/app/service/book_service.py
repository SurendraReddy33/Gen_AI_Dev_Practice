import json
import os
from app.utils.decorators import handle_exceptions
from app.utils.logger import get_logger

logger = get_logger(__name__)
BOOK_FILE = "app/data/books.json"

@handle_exceptions
def load_books():
    if not os.path.exists(BOOK_FILE):
        return []
    with open(BOOK_FILE, 'r') as f:
        return json.load(f)

@handle_exceptions
def save_books(books):
    with open(BOOK_FILE, 'w') as f:
        json.dump(books, f, indent=4)
    logger.info("Books data saved")

@handle_exceptions
def add_book(book: dict):
    books = load_books()
    books.append(book)
    save_books(books)
    return {"message": "Book added successfully"}

@handle_exceptions
def update_book(book_id, UpdateBook):
    books = load_books()
    updated = False
    for book in books:
        if book.get("book_id") == book_id:
            book.update(UpdateBook)
            updated = True
            break
    if updated:
        save_books(books)
        return {"message": "Book updated successfully"}
    return {"message": "Book ID not found"}

@handle_exceptions
def list_books():
    return load_books()

@handle_exceptions
def delete_book(book_id):
    books = load_books()
    updated = [b for b in books if b.get("book_id") != book_id]
    if len(updated) == len(books):
        return {"message": "Book not found"}
    save_books(updated)
    return {"message": "Book deleted successfully"}

@handle_exceptions
def search_books_by_title(title):
    books = load_books()
    result = [b for b in books if title.lower() in b.get("title", "").lower()]
    return result if result else {"message": "No book found with that title"}
