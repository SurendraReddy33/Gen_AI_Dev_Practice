class Book:
    def __init__(self, book_id, title, author, category, available=True):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.available = available

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "available": self.available
        }
    
    @classmethod
    def from_dict(cls, data):
        if isinstance(data, dict):
            return cls(
                book_id= data.get("book_id"),
                title = data.get("title"),
                author = data.get("author"),
                category = data.get("category")
            )
        elif isinstance(data, Book):
            return data
    
