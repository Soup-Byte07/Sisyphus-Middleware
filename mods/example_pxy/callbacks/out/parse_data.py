import json
from core.logging.logging import custom_message
# Returns a JSON object if the string is a valid JSON, otherwise returns the string with an error message.
# Example:
# str_to_json('{"key": "value"}') -> {'key': 'value'}
# str_to_json('invalid json') -> 'invalid json##### Is not a valid JSON #####'
def str_to_json(x: str) -> str:
    try:
        return json.loads(x)
    except json.JSONDecodeError:
        custom_message(f"Invalid JSON: {x} - Is not a valid JSON", "error")
        return x + " ::: Is not a valid JSON"

