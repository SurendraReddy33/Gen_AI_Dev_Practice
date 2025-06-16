import json
from app.model.employee import Employee
from app.utils.decoratores import handle_exceptions
from app.utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

EMPLOYEE_DATA_FILE = "app/data/employees_details.json"

@handle_exceptions[]
def load_employees():
    logger.info(f"INITIALIZATION: Starting to load employee data from file: {EMPLOYEE_DATA_FILE}")
    try:
        with open (EMPLOYEE_DATA_FILE, 'r') as f:
            employees_data = json.load(f)
            logger.info(f"DATA LOAD: Successfully read {len(employees_data)} employee records from JSON file")
            
            # Log sample of first employee record (with sensitive fields masked)
            if employees_data:
                sample = employees_data[0].copy()
                if 'salary' in sample:
                    sample['salary'] = '******'
                if 'dob' in sample:
                    sample['dob'] = '****-**-**'
                logger.info(f"DATA SAMPLE: First record structure: {sample}")
            
            employees = [Employee(**emp) for emp in employees_data]
            
            # Log departments statistics
            if employees:
                departments = {}
                for emp in employees:
                    dept = emp.department
                    departments[dept] = departments.get(dept, 0) + 1
                logger.info(f"STATISTICS: Department distribution: {departments}")
                
            logger.info(f"INITIALIZATION COMPLETE: Created {len(employees)} Employee objects successfully")
            return employees
    except Exception as e:
        logger.error(f"INITIALIZATION ERROR: Failed to load employees: {str(e)}")
        raise

employees = load_employees()

def get_all_employees():
    logger.info(f"API REQUEST: Retrieving complete employee dataset containing {len(employees)} records")
    result = [emp.to_dict() for emp in employees]
    logger.info(f"API RESPONSE: Returning {len(result)} employee records with {sum(len(emp.get('projects', [])) for emp in result)} total projects")
    return result

def get_bench_employees():
    logger.info(f"API REQUEST: Filtering for bench employees from total {len(employees)} employees")
    bench_employees = list(filter(lambda e: e.is_on_bench(), employees))
    result = [emp.to_dict() for emp in bench_employees]
    
    # Calculate percentage of workforce on bench
    bench_percentage = (len(bench_employees) / len(employees)) * 100 if employees else 0
    
    logger.info(f"STATISTICS: Found {len(bench_employees)} employees on bench ({bench_percentage:.2f}% of workforce)")
    
    # Log department-wise bench distribution if bench employees exist
    if bench_employees:
        departments = {}
        for emp in bench_employees:
            dept = emp.department
            departments[dept] = departments.get(dept, 0) + 1
        logger.info(f"DETAILED BREAKDOWN: Bench employees by department: {departments}")
        
    logger.info(f"API RESPONSE: Returning {len(result)} bench employee records")
    return result

def get_by_project_status(status):
    logger.info(f"API REQUEST: Filtering employees by project status: '{status}'")
    filtered_employees = [emp for emp in employees if emp.has_project_with_status(status)]
    result = [emp.to_dict() for emp in filtered_employees]
    
    # Calculate percentage of workforce with this project status
    status_percentage = (len(filtered_employees) / len(employees)) * 100 if employees else 0
    
    # Count total projects with this status
    project_count = 0
    for emp in filtered_employees:
        for proj in emp.projects:
            if proj.status == status:
                project_count += 1
    
    # Log detailed statistics
    logger.info(f"STATISTICS: Found {len(filtered_employees)} employees ({status_percentage:.2f}% of workforce) with {project_count} '{status}' projects")
    
    # Log department-wise distribution if employees exist
    if filtered_employees:
        departments = {}
        for emp in filtered_employees:
            dept = emp.department
            departments[dept] = departments.get(dept, 0) + 1
        logger.info(f"DETAILED BREAKDOWN: Employees with '{status}' projects by department: {departments}")
    
    logger.info(f"API RESPONSE: Returning {len(result)} employee records with '{status}' projects")
    return result
