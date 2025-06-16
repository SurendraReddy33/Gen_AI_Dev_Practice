from app.service.employee_service import get_all_employees, get_bench_employees, get_by_project_status
from flask import Flask, jsonify, request
from app.utils.logger import get_logger

# Initialize logger with application names
logger = get_logger('employee_api.main')

app = Flask(__name__)

@app.route("/")
def index():
    logger.info(f"API REQUEST: Health check requested from IP: {request.remote_addr}, User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    return {"Status" : "Employee API is Running as Expected. State = Healthy"}

@app.route("/employees", methods=["GET"])
def all_employees(): # List All Employees
    request_id = id(request)
    logger.info(f"API REQUEST [{request_id}]: All employees endpoint called from IP: {request.remote_addr}, User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    
    employees = get_all_employees()
    
    logger.info(f"API RESPONSE [{request_id}]: Returning {len(employees)} employees with HTTP 200 status")
    return jsonify(employees), 200

@app.route("/employees/bench", methods=["GET"])
def bench_employees(): # Find All Employees On Bench
    request_id = id(request)
    logger.info(f"API REQUEST [{request_id}]: Bench employees endpoint called from IP: {request.remote_addr}, User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    
    employees = get_bench_employees()
    
    logger.info(f"API RESPONSE [{request_id}]: Returning {len(employees)} bench employees with HTTP 200 status")
    return jsonify(employees), 200

@app.route("/employees/active_projects", methods=["GET"])
def active_projects(): # Find All Employees With Active Projects
    request_id = id(request)
    logger.info(f"API REQUEST [{request_id}]: Active projects endpoint called from IP: {request.remote_addr}, User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    
    employees = get_by_project_status("active")
    
    logger.info(f"API RESPONSE [{request_id}]: Returning {len(employees)} employees with active projects with HTTP 200 status")
    return jsonify(employees), 200

@app.route("/employees/completed_projects", methods=["GET"])
def completed_projects(): # Find All Employees With Completed Projects
    request_id = id(request)
    logger.info(f"API REQUEST [{request_id}]: Completed projects endpoint called from IP: {request.remote_addr}, User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    
    employees = get_by_project_status("completed")
    
    logger.info(f"API RESPONSE [{request_id}]: Returning {len(employees)} employees with completed projects with HTTP 200 status")
    return jsonify(employees), 200


if __name__ == "__main__":
    logger.info("SERVER STARTUP: Initializing Employee API server")
    logger.info(f"SERVER CONFIG: Debug mode: {app.debug}, Host: 127.0.0.1, Port: 5000")
    
    # Register available endpoints for logging
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(f"{rule.endpoint} [{', '.join(rule.methods)}] {rule}")
    
    logger.info(f"SERVER ROUTES: Available endpoints: {routes}")
    logger.info("SERVER READY: Employee API server is ready to accept requests")
    
    app.run(debug=True)