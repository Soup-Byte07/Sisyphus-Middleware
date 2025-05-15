from core.logging.logging import custom_message
import json
def funny_haha_example(input):
    print(input)
    custom_message("This is a funny ahah, very peak!", "info")
    input = json.loads(input)
    input["funny"] = "haha"
    return input

