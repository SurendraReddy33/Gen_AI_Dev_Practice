from fastapi import APIRouter
from app.services.appointment_service import (
    add_appointment, update_appointment, list_appointments,
     delete_appointment
)
from app.models.appointment import Appointment

router = APIRouter()

@router.post("/add")
def create_appointment(appointment: Appointment):
    return add_appointment(appointment.dict())

@router.put("/update/{appointment_id}")
def modify_appointment(appointment_id: str, appointment: Appointment):
    return update_appointment(appointment_id, appointment)

@router.get("/view_all")
def read_all_appointments():
    return list_appointments()

@router.delete("/delete/{appointment_id}")
def remove_appointment(appointment_id: str):
    return delete_appointment(appointment_id)


