from pydantic import BaseModel
from typing import Optional

class Patient(BaseModel):
    patient_id: str
    name: str
    age: str
    gender: str
    disease: Optional[str] = None

