import logging
from logging.handlers import RotatingFileHandler

def get_logger(name):
    # Get or create a logger with the given name
    logger = logging.getLogger(name)
    
    # Set the log level to INFO
    logger.setLevel(logging.INFO)

    # Avoid adding multiple handlers if already configured
    if not logger.handlers:
        # Formatter for both handlers
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s"
        )

        # Rotating file handler
        file_handler = RotatingFileHandler(
            "user_login_api.log", maxBytes=10_000_000, backupCount=10, encoding='utf-8'
        )
        file_handler.setFormatter(formatter)

        # Stream handler (logs to console)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        # Add both handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger