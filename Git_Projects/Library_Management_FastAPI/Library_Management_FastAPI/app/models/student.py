from pydantic import BaseModel
from typing import Optional, Union

class Student(BaseModel):
    student_id: str
    name: str
    department: Optional[str] = None
    year: Union[int, str]
