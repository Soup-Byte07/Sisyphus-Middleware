import sys
from core.logging.logging import custom_message

def exit_with_custom_message(message: str, type: str):
    custom_message(message, type)
    sys.exit(1)

