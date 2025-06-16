from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

import logging
import json

logging.basicConfig(
    filename= 'employee_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


logging = logging.getLogger(__name__)

app = FastAPI(title="Employee Search API")

class Project(BaseModel):
    project_id : str
    name : str 
    status : str

class Employee(BaseModel):
    emp_id : str
    name: str
    department : str
    salary : int
    designation : str
    location : str
    dob : str
    projects : list[Project]

class LoginRequest(BaseModel):
    username: str
    password: str


# ------ Load Employee data -------
with open("employees_details.json","r") as f:
    raw_employees = json.load(f)
employees = [ Employee (**emp) for emp in raw_employees]

@app.post("/login")
async def login_user(data: LoginRequest):
    if data.username == "Surendra" and data.password == "Reddy":
        return {"message": "Login Successful"}
    raise HTTPException(status_code=401, detail="Login Failed")

@app.get("/employees", response_model = list[Employee])
async def get_all_employees():
    return employees

@app.get("employees/bench", response_model = list[Employee])
async def get_employees_on_bench():
    return employees


@app.get("employees/project-status/{status}", response_model = list[Employee])
async def get_employees_by_project_status(status: str):
    return [emp for emp in employees if any (p.status == status for p in emp.projects)]

