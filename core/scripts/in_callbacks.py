from core.logging.logging import custom_message
import json

def input_example(input):
    custom_message("Changing Input!", "info")
    input["title"] = "Well this is even more funny"
    return input
