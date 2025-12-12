from pydantic import BaseModel
from typing import Optional

class Patient(BaseModel):
    patient_id: str
    name: str
    age: str
    gender: str
    disease: Optional[str] = None


class UpdatePatient(BaseModel):
    patient_id: str
    name: Optional[str]
    age: Optional[str]
    gender: Optional[str] = None
    disease: Optional[str] = None


