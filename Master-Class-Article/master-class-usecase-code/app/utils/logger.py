import logging
from logging.handlers import RotatingFileHandler  

def get_logger(name):
    
    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    #Prevent adding handlers multiple times (common when get_logger is called repeatedly).

    if not logger.handlers:
        # define the log message format.
        formatter = logging.Formatter(
             "%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s"
        )

        file_handlers = RotatingFileHandler(
            "usecase.log",maxBytes=100_000_00,backupCount=10,encoding="utf-8"
        )

        file_handlers.setFormatter(formatter) # Apply the formatter to the file handler

        # stream handler (console output)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        # Attach both handlers to the logger
        logger.addHandler(file_handlers)
        logger.addHandler(stream_handler)

    #Return the configured to the logger
    return logger