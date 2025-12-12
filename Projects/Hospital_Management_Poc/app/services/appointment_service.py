import json
import os
from app.models.appointment import Appointment
from app.utils.decorators import handle_exceptions
from app.utils.logger import get_logger

logger = get_logger(__name__)
APPOINTMENT_FILE = "app/data/appointments.json"

@handle_exceptions
def load_appointments():
    if not os.path.exists(APPOINTMENT_FILE):
        return []
    with open(APPOINTMENT_FILE, 'r') as f:
        return json.load(f)

@handle_exceptions
def save_appointments(appointments):
    with open(APPOINTMENT_FILE, 'w') as f:
        json.dump(appointments, f, indent=4)
    logger.info("appointments data saved")

@handle_exceptions
def add_appointment(appointment: dict):
    appointments = load_appointments()
    appointments.append(appointment)
    save_appointments(appointments)
    return {"message": "appointment added successfully"}

@handle_exceptions
def update_appointment(appointment_id, UpdateAppointment):
    appointments = load_appointments()
    updated = False
    for a in appointments:
        if a.get("appointment_id") == appointment_id:
            a.update(UpdateAppointment)
            updated = True
            break
    if updated:
        save_appointments(appointments)
        return {"message": "appointment updated successfully"}
    return {"message": "appointment ID not found"}

@handle_exceptions
def list_appointments():
    return load_appointments()

@handle_exceptions
def delete_appointment(appointment_id):
    appointments = load_appointments()
    updated = [a for a in appointments if a.get("appointment_id") != appointment_id]
    if len(updated) == len(appointments):
        return {"message": "appointment not found"}
    save_appointments(updated)
    return {"message": "appointment deleted successfully"}

