import json
import os
from app.utils.decorators import handle_exceptions
from app.utils.logger import get_logger
from app.models.book import Book

logger = get_logger(__name__)
BOOK_FILE = "app/data/books.json"

@handle_exceptions
def load_books():
    if not os.path.exists(BOOK_FILE):
        return []
    with open(BOOK_FILE, 'r') as f:
        books_data = json.load(f)
        return [Book.from_dict(b) for b in books_data]
    
@handle_exceptions
def save_books(books):
    with open (BOOK_FILE, 'w') as f:
        json.dump([book.to_dict() for book in books], f, indent = 4)
    logger.info("Books data saved")

@handle_exceptions
def add_book(book: Book):
    books = load_books()
    books.append(book)
    save_books(books)
    print("Book added successfully")

@handle_exceptions
def update_book(book_id, updated_data):
    books = load_books()
    books = [Book.from_dict(b) for b in books]
    updated = False
    for i, book in enumerate(books):
        if str(book.book_id) == str(book_id):
            for key, value in updated_data.items():
                if hasattr(book, key):
                    setattr(book, key, value)
            updated = True
            break
    if updated:
        save_books(books)
        print("Books data updated successfully")
    else:
        print("Book ID not Found")  

@handle_exceptions
def list_books():
    books = load_books()
    if not books:
        print("No books available")
    for book in books:
        status = "Available" if book.available else "Issued"
        print(f"{book.book_id} - {book.title} - {book.author} - {book.category} - {status}")

@handle_exceptions
def search_books_by_title(title):
    books = load_books()
    found = False
    for book in books:
        if title.lower() in book.title.lower():
            status = "Available"  if book.available else "Issued"
            print(f"{book.book_id} - {book.title} - {book.author} - {book.category} - {status}")
            found = True
    if not found:
        print("No book found with that title")

@handle_exceptions
def delete_book(book_id):
    books = load_books()
    updated = [b for b in books if b.book_id != book_id]
    if len(updated) == len(books):
        print("Book not found")
    else:
        save_books(updated)
        print("Book deleted")

