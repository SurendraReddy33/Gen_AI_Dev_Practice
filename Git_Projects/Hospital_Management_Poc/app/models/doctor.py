from pydantic import BaseModel
from typing import Optional

class Doctor(BaseModel):
    doctor_id: str
    name: str
    speciality: Optional[str] = None
    available: bool = True


