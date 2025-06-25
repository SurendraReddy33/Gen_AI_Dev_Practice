from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    book_id: str
    title: str
    author: str
    category: Optional[str] = None
    available: bool = True
