import json


def load_json(file_to_parse):
    with open(file_to_parse) as json_data:
        json_string = json.load(json_data)
    return json_string
