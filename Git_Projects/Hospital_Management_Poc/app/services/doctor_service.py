import json
import os
from app.models.doctor import Doctor
from app.utils.decorators import handle_exceptions
from app.utils.logger import get_logger

logger = get_logger(__name__)
DOCTOR_FILE = "app/data/doctors.json"

@handle_exceptions
def load_doctors():
    if not os.path.exists(DOCTOR_FILE):
        return []
    with open(DOCTOR_FILE, 'r') as f:
        return json.load(f)

@handle_exceptions
def save_doctors(doctors):
    with open(DOCTOR_FILE, 'w') as f:
        json.dump(doctors, f, indent=4)
    logger.info("doctors data saved")

@handle_exceptions
def add_doctor(doctor: dict):
    doctors = load_doctors()
    doctors.append(doctor)
    save_doctors(doctors)
    return {"message": "doctor added successfully"}

@handle_exceptions
def update_doctor(doctor_id, UpdateDoctor):
    doctors = load_doctors()
    updated = False
    for d in doctors:
        if d.get("doctor_id") == doctor_id:
            d.update(UpdateDoctor)
            updated = True
            break
    if updated:
        save_doctors(doctors)
        return {"message": "doctor updated successfully"}
    return {"message": "doctor ID not found"}

@handle_exceptions
def list_doctors():
    return load_doctors()

@handle_exceptions
def delete_doctor(doctor_id):
    doctors = load_doctors()
    updated = [d for d in doctors if d.get("doctor_id") != doctor_id]
    if len(updated) == len(doctors):
        return {"message": "doctor not found"}
    save_doctors(updated)
    return {"message": "doctor deleted successfully"}


