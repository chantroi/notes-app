import re
import random
import names


def sanitize(input_string):
    sanitized_string = re.sub(r"[^a-zA-Z0-9_]", "", input_string)
    sanitized_string = sanitized_string.lstrip("_")
    return sanitized_string


def extract_raw(input_string):
    start_index = input_string.find("<code>")
    end_index = input_string.find("</code>")
    if start_index != -1 and end_index != -1:
        content = input_string[start_index + len("<code>") : end_index]
        return content
    return None


def generate_name():
    full_name = names.get_full_name()
    full_name = sanitize(full_name)
    first_name = names.get_first_name()
    return random.choice([full_name, first_name])
