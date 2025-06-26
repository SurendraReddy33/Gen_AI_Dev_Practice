from fastapi import APIRouter
from app.service.book_service import (
    add_book, update_book, list_books,
    search_books_by_title, delete_book
)
from app.models.book import Book, UpdateBook

router = APIRouter()

@router.post("/add")
def create_book(book: Book):
    return add_book(book.dict())

@router.put("/update/{book_id}")
def modify_book(book_id: str, book: UpdateBook):
    return update_book(book_id, book)

@router.get("/view_all")
def get_all_books():
    return list_books()

@router.delete("/delete/{book_id}")
def remove_book(book_id: str):
    return delete_book(book_id)

@router.get("/search/{title}")
def search_book(title: str):
    return search_books_by_title(title)
