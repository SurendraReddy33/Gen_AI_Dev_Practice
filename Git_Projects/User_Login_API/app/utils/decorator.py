from functools import wraps
from fastapi import HTTPException
from app.utils.logger import get_logger
import asyncio

logger=get_logger(__name__)


# creating an function for excpetion handling
def handle_exceptions(func):
    # The decorator that wraps the original function
    @wraps(func)# This decorator preserves the original function's name and docstring

    async def wrapper(*args,**kwargs):
        try:
            logger.info(f"Executing: {func.__name__}")
            # Trying to execute original function
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
            
        # If an exception occurs, handle it by returning a custom error message
        except Exception as e:
            logger.exception(f"Error while Executing: {func.__name__} : {e}")
            raise HTTPException(status_code = 400,detail= str(e))
    return wrapper
 