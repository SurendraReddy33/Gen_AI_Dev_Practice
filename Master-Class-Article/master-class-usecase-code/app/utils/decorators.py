from functools import wraps
from fastapi import HTTPException



# creating an function for excpetion handling
def handle_exceptions(func):
    # The decorator that wraps the original function

    @wraps(func)# This decorator preserves the original function's name and docstring
    def wrapper(*args,**kwargs):
        try:
           
            # Trying to execute original function
            return func(*args,**kwargs)
        # If an exception occurs, handle it by returning a custom error message
        except Exception as e:
           
            raise HTTPException(status_code = 400,detail= str(e))
    return wrapper