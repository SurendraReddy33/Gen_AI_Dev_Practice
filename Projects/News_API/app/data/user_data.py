from app.utils.decorators import handle_exceptions
from app.utils.logger import get_logger
import os,json

logging = get_logger(__name__)

@handle_exceptions
def save_to_json(data, filename):
    """
    Saves the processed data to a JSON file.
    Automatically creates the directory if it does not exist.
    """
    dir_name = os.path.dirname(filename)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logging.info(f"Saved output to {filename}")