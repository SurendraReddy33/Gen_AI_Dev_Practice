import functools
import traceback
from utils.helpers import logger

def log_exception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Entering the function : {func.__name__}")
        try:
            result = func(*args, **kwargs) # invoke calling function
            logger.debug(f"Exiting the function : {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"An error occurred in the function : {func.__name__} : Trace {e}")
    return wrapper

