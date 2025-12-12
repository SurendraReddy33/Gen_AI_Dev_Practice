from fastapi import APIRouter
from app.services.doctor_service import (
    add_doctor, update_doctor, list_doctors,
     delete_doctor
)
from app.models.doctor import Doctor

router = APIRouter()

@router.post("/add")
def create_appointment(doctor: Doctor):
    return add_doctor(doctor.dict())

@router.put("/update/{doctor_id}")
def modify_doctor(doctor_id: str, doctor: Doctor):
    return update_doctor(doctor_id, Doctor)

@router.get("/view_all")
def read_all_doctors():
    return list_doctors()

@router.delete("/delete/{doctor_id}")
def remove_doctor(doctor_id: str):
    return delete_doctor(doctor_id)


