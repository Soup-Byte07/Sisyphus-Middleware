import logging
import logging

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)

def custom_message(message: str, type: str = "info"):
    
    if(type == "info"):
        logger.info(message)
    elif(type == "debug"):
        logger.debug(message)
    elif(type == "warning"):
        logger.warning(message)
    elif(type == "error"):
        logger.error(message)
    elif(type == "critical"):
        logger.critical(message)
    else:
        logger.info(message)

def change_method_color(method: str):
    if method == "GET":
        method = f"\033[92m{method}\033[0m"  # Green
    elif method == "POST":
        method = f"\033[94m{method}\033[0m"  # Blue
    elif method == "PUT":
        method = f"\033[93m{method}\033[0m"  # Yellow
    elif method == "DELETE":
        method = f"\033[91m{method}\033[0m"  # Red
    else:
        method = f"\033[0m{method}\033[0m"  # Default color

    return method

def check_post_require(method, data):
    if(method =="POST" and data is None):
        method = change_method_color(method)
        logger.info(f"{method} is missing a request body: {data}")
        raise ValueError(f"{method} request requires data.")
        
def log_route_creation(route: str, method: str, message: str = ""):
    logger.info(f"Created Route: {route} with method: {change_method_color(method)} {message}")
