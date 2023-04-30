import json

def read_message_file(file_to_parse):
    with open(file_to_parse) as json_data:
        json_string = json.load(json_data)
    participants = json_string['participants']
    messages = json_string['messages']
    return {messages: messages, participants: participants}


def load_json(file_to_parse):
    with open(file_to_parse) as json_data:
        json_string = json.load(json_data)
    return json_string

def encode_string(string):
    try:
        return string.encode('latin1').decode('utf8')
    except (UnicodeEncodeError, UnicodeDecodeError) as e:
        print(f'Failed to encode {string}: \t{e}')
        return string

def get_participants(json_string):
    participants = []
    for name in json_string:
        participants.append(name['name'])
    return participants

def get_your_name():
    return load_json('your_name.json').name