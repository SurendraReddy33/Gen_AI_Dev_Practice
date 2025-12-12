from functools import wraps
import time
from flask import request
from app.utils.logger import logger

def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return ({"Error": str(e)}), 500
    return wrapper

