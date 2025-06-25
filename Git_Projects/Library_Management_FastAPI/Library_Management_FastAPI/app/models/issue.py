from pydantic import BaseModel
from typing import Optional

class IssueRecord(BaseModel):
    student_id: str
    book_id: str
    issue_date: str
    return_date: Optional[str] = None
