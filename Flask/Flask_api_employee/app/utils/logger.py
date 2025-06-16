import logging
def logger(name):
    logger = logging.getLogger(name)

    if not logger.handlers:
        file_handler = logging.FileHandler("employee_api.log")

        console_handler = logging.StreamHandler()

        format = '%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(funcName)s() | [%(threadname)s] | %(message)s '
        formatter = logging.Formatter(format, datefmt = '%Y-%m-%d %H:%M:%S')

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        logger.setLevel(logging.INFO)

    return logger