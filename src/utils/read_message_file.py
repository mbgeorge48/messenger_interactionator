import json


def read_message_file(file_to_parse):
    print(f"reading {file_to_parse}")
    with open(file_to_parse) as json_data:
        json_string = json.load(json_data)
    return {
        "messages": json_string["messages"],
        "participants": json_string["participants"],
    }
