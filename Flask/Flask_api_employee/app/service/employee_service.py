import json
from app.model.employee import Employee
from app.utils.decorators import handle_exceptions
from app.utils.logger import logger

Logger = logger(__name__)

EMPLOYEE_DATA = "app/data/employee_details.json"

@handle_exceptions
def load_employees():
    Logger.info(f"INITIALIZATION : Starting to load employee data from file: {EMPLOYEE_DATA}")
    try:
        with open(EMPLOYEE_DATA, "r") as f:
            employees_data = json.load(f)
            logger.info(f"DATA LOAD: Successfully loaded {len(employees_data)} employee records from json file")

            if employees_data:
                sample = employees_data[0].copy()
                if 'salary' in sample:
                    sample['salary'] = '*****'
                if 'dob' in sample:
                    sample['dob'] = '*****'
                logger.info(f"Sample : first record structure {sample}")

            employees = [Employee(**emp) for emp in employees_data]


            if employees:
                departments = {}
                for emp in employees:
                    dept = emp.department
                    departments[dept] = departments.get(dept, 0) + 1
                logger.info(f"Statistics: Department distribution: {departments}")

            logger.info(f"Initialization Complete : created {len(employees)} employee objects successfully")
            return employees
        
    except Exception as e:
        logger.error(f"Initialization Error : Failed to load employees: {str(e)}")
        raise

employees = load_employees()


def get_all_employees():
    logger.info(f"Request: Retreives total employee records: {len(employees)}")
    result = [emp.convert_to_dict() for emp in employees]
    logger.info(f"Response : Total Employee records {len(result)} with {sum(len(emp.get('projects', [])) for emp in result)} total projects ")
    return result


def get_benched_employees():
    logger.info(f"Request: Getting Benched Employees from {len(employees)} employees")
    benched_employees = list(filter(lambda e: e.benched_emps(), employees))
    result = [emp.convert_to_dict() for emp in benched_employees]

    bench_percentage = (len(benched_employees) / len(employees)) * 100 if employees else 0

    logger.info(f"Result: Found {len(benched_employees)} employees in bench with ({bench_percentage:.2f} of workforce)")

    if benched_employees:
        departments={}
        for emp in benched_employees:
            dept = emp.department
            departments[dept] = departments.get(dept, 0) + 1
        logger.info(f"Benched Employees by department : {departments}")

    logger.info(f"Response: Total bench employee records {len(result)}")
    return result

def emp_project_status(status):
    logger.info(f"Request: Filtering Employees by project status: '{status}'")
    filtered_employees = [emp for emp in employees if emp.project_status(status)]
    result = [emp.convert_to_dict() for emp in filtered_employees]

    status_percentage = (len(filtered_employees) / len(employees)) * 100 if employees else 0

    project_count = 0
    for emp in filtered_employees:
        for project in emp.projects:
            if project.status == status:
                project_count += 1

    logger.info(f"Result: Found {len(filtered_employees)} Employees with ({status_percentage:.2f} of workforce) {project_count} '{status}' projects ")

    if filtered_employees:
        departments = {}
        for emp in filtered_employees:
            dept = emp.department
            departments[dept] = departments.get(dept, 0) + 1
        logger.info(f"Employees with '{status}' projects by department: {departments}")

    logger.info(f"Response: Total Employee Records : {len(result)} with '{status}' projects")
    return result


    