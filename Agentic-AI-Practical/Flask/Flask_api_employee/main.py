from app.service.employee_service import get_all_employees, get_benched_employees, emp_project_status
from flask import Flask, jsonify, request
from app.utils.logger import logger

Logger = logger('employee.api.main')

app = Flask(__name__)

@app.route("/")
def index():
    Logger.info(f"Request: checking sample")
    return {"Status: Employee API is Running"}


if __name__ == "__main__":
    app.run(debug=True)