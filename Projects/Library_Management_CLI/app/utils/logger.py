import logging
import os
from logging.handlers  import RotatingFileHandler  # For controlling the log file size and reusing it.

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    log_dir = "logs"
    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_path = os.path.join(log_dir, "library_management_api.log")

    file_handler = RotatingFileHandler(
        log_path, maxBytes=1_000_000, backupCount=3
    )
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger