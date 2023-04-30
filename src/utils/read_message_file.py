import json


def read_message_file(file_to_parse):
    with open(file_to_parse) as json_data:
        json_string = json.load(json_data)
    participants = json_string['participants']
    messages = json_string['messages']
    return {messages: messages, participants: participants}