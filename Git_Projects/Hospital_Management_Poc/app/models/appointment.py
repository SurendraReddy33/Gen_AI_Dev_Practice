from pydantic import BaseModel
from typing import Optional

class Appointment(BaseModel):
    appointment_id: str
    patient_id: str
    doctor_id: str
    appointment_date: str
    status: Optional[str] = "Scheduled"

class UpdateAppointment(BaseModel):
    appointment_id: str
    patient_id: str
    doctor_id: str
    appointment_date: Optional[str] = None
    status: Optional[str] = None


