import json
import os
from app.models.patient import Patient
from app.utils.decorators import handle_exceptions
from app.utils.logger import get_logger

logger = get_logger(__name__)
PATIENT_FILE = "app/data/patients.json"

@handle_exceptions
def load_patients():
    if not os.path.exists(PATIENT_FILE):
        return []
    with open(PATIENT_FILE, 'r') as f:
        return json.load(f)

@handle_exceptions
def save_patients(patients):
    with open(PATIENT_FILE, 'w') as f:
        json.dump(patients, f, indent=4)
    logger.info("patients data saved")

@handle_exceptions
def add_patient(patient: dict):
    patients = load_patients()
    patients.append(patient)
    save_patients(patients)
    return {"message": "Patient added successfully"}

@handle_exceptions
def update_patient(patient_id, UpdatePatient):
    patients = load_patients()
    updated = False
    for p in patients:
        if p.get("patient_id") == patient_id:
            p.update(UpdatePatient)
            updated = True
            break
    if updated:
        save_patients(patients)
        return {"message": "patient updated successfully"}
    return {"message": "Patient ID not found"}

@handle_exceptions
def get_all_patients():
    return load_patients()

@handle_exceptions
def delete_patient(patient_id):
    patients = load_patients()
    updated = [p for p in patients if p.get("patient_id") != patient_id]
    if len(updated) == len(patients):
        return {"message": "patient not found"}
    save_patients(updated)
    return {"message": "patient deleted successfully"}


