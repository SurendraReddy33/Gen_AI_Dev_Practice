"""Logging utility for the Employee API application.

This module provides functionality to create and configure loggers
for different components of the application. It ensures consistent
log formatting and behavior across the entire codebase.
"""

import logging

def get_logger(name):
    """Create and configure a logger for a specific module.
    
    This function creates a named logger with file-based logging configured
    to output to 'employee_api.log'. It ensures that each logger is only
    configured once by checking if handlers already exist.
    
    The logger is configured with a detailed format that includes:
    - Timestamp with millisecond precision
    - Log level
    - Module name
    - Line number
    - Function name
    - Thread ID
    - Actual log message
    
    Args:
        name (str): The name for the logger, typically __name__ from the calling module
        
    Returns:
        logging.Logger: A configured logger instance
        
    Example:
        # In a module file
        from app.utils.logger import get_logger
        
        # Create a logger for this module
        logger = get_logger(__name__)
        
        # Use the logger
        logger.info('This is an informational message')
        logger.error('This is an error message')
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Create file handler
        file_handler = logging.FileHandler("employee_api.log")
        
        # Create console handler for immediate feedback
        console_handler = logging.StreamHandler()
        
        # Create a detailed formatter
        detailed_format = '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(funcName)s() | [%(threadName)s] | %(message)s'
        # Use a simpler date format that's compatible with the standard library
        formatter = logging.Formatter(detailed_format, datefmt='%Y-%m-%d %H:%M:%S')
        
        # Set formatter for both handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # Set log level
        logger.setLevel(logging.INFO)
    return logger