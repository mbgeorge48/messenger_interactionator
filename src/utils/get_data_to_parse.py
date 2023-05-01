import os
import utils


def get_data_to_parse(data_to_parse):
    data=[]

    for file in data_to_parse:
        data.append(utils.read_message_file(file))
    participants = messages = []
    for entry in data:
        participants=participants + utils.get_participants(entry["participants"])
        messages=messages + entry["messages"]
    participants=list(dict.fromkeys(participants))
    return messages, participants