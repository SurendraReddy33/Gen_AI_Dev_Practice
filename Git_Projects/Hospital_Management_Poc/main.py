from fastapi import FastAPI
from app.routers import patient_router, doctor_router, appointment_router

app = FastAPI(title = "Hospital Management System")

app.include_router(patient_router.router, prefix="/patients")
app.include_router(doctor_router.router, prefix="/doctors")
app.include_router(appointment_router.router, prefix="/appointments")

@app.get("/")
def root():
    return {"message": "Welcome to the Hospital Manegement API"}
