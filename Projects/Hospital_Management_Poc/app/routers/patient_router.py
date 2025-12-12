from fastapi import APIRouter
from app.services.patient_service import (
    add_patient, update_patient, get_all_patients, delete_patient
)
from app.models.patient import Patient

router = APIRouter()

@router.post("/add")
def create_patient(patient: Patient):
    return add_patient(patient.dict())

@router.put("/update/{patient_id}")
def modify_patient(patient_id: str, patient: Patient):
    return update_patient(patient_id, patient)

@router.get("/list")
def read_all_patients():
    return get_all_patients()

@router.delete("/delete/{patient_id}")
def remove_patient(patient_id: str):
    return delete_patient(patient_id)

