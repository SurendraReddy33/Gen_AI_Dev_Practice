from fastapi import APIRouter
from app.service.book_service import (
    add_book, update_book, list_books,
    search_books_by_title, delete_book
)
from app.models.book import Book

router = APIRouter()

@router.post("/books/add")
def create_book(book: Book):
    return add_book(book.dict())

@router.put("/books/update")
def modify_book(book_id: str, updates: dict):
    return update_book(book_id, updates)

@router.get("/books")
def get_all_books():
    return list_books()

@router.delete("/books/delete")
def remove_book(book_id: str):
    return delete_book(book_id)

@router.get("/books/search/")
def search_book(title: str):
    return search_books_by_title(title)
