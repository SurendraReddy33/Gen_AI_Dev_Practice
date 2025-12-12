from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    book_id: str
    title: str
    author: str
    category: Optional[str] = None
    available: bool

class UpdateBook(BaseModel):
    book_id: str
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    available: Optional[bool] = None
