import json
import os
import logging

#Logger COnfiguration
logger = logging.getLogger("emp_logger")
logger.setLevel(logging.DEBUG)
logger.propagate = False

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(log_dir, exist_ok=True) # create the logs directory if does not exist

log_file = os.path.join(log_dir, "actions.log")
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

# custom log formatting {Time} - {Level} - {Message}
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s |  %(levelname)s | %(module)s | %(funcName)s | line:%(lineno)d | %(message)s '
))
if not logger.handlers:
    logger.addHandler(file_handler)


def save_to_json(data, file):
    """save a list of dictionaries to a JSON file"""
    try:
        with open(file, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info("saved data to the file: {file}")

    except Exception as e:
        logger.exception(f"Failed to save {file} : Error : {e}")



def load_from_json(file):
    """Load and return a list of dictionaries from a JSON file"""
    try:
        if not os.path.exists(file):
            logger.warning(f"JSON file not found, returning empty list : {file}")
            return []
        with open(file, 'r') as f:
            data = json.load(f)
            print(f"Loaded data from JSON file : ")
            logger.info(f"Loaded data from JSON File : {file}")
            return data
    except Exception as e:
        logger.exception(f"Failed to load from {file} : {e}")
        return []