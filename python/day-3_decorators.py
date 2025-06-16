def log_action(func):
    def wrapper(*args, **kwargs):
        print(f" Running {func.__name__} with args {args} and kwargs {kwargs}")
        result = func(*args, **kwargs)
        print(f"completed {func.__name__}")
        return result
    return wrapper

#sample employee data
employees = [
    {'name': 'Alice', 'dept': 'HR'},
    {'name': 'Bob', 'dept': 'Tech'},
    {'name': 'Charlie', 'dept': 'Tech'},
    {'name': 'David', 'dept': 'Admin'}
]

#function to filter employees by department
@log_action
def get_employees_by_dept(dept):
    return list(filter(lambda e: e['dept'] == dept, employees))

#call decorated function
tech_team = get_employees_by_dept('Tech')
print("Tech Department employees :", tech_team)