import json


def read_from_file(file_name):
    """
    Reads text from a file
    """
    with open(file_name, "r") as text_file:
        return text_file.read()


def from_json_file(file_name):
    json_content = read_from_file(file_name)
    return json.loads(json_content)
