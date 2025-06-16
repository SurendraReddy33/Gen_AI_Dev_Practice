from functools import wraps
from app.utils.logger import get_logger

logger=get_logger(__name__)

def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            logger.info(f"Executing: {func.__name__}")
            return func(*args,**kwargs)
        except Exception as e:
            logger.exception(f"Error while Executing: {func.__name__} : {e}")
            print("Something went wrong")
    return wrapper
