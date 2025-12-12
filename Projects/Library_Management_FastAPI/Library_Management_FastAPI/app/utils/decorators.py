from functools import wraps
from app.utils.logger import get_logger

logger = get_logger(__name__)

def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info(f"Executing: {func.__name__}")
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"Error in {func.__name__}: {e}")
            return {"error": f"An error occurred in {func.__name__}"}
    return wrapper
