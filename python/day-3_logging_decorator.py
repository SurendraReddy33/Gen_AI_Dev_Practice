import traceback

def log_exceptions_to_file(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            with open("error_log.txt", "a") as f:
                f.write(f"\nException in {func.__name__}:\n")
                f.write(traceback.format_exc())
            print(f"Error logged from {func.__name__}")
            raise
    return wrapper


@log_exceptions_to_file
def divide_salary_by_employees(salary, count):
    return salary / count

try:
    divide_salary_by_employees(50000,0)
except:
    pass #use pass only when already logged