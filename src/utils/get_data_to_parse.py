from utils import get_participants, read_message_file


def get_data_to_parse(data_to_parse):
    data=[]
    for file in data_to_parse:
        data.append(read_message_file(file))

    for entry in data:
        participants=participants + get_participants(entry["participants"])
        messages=messages + entry["messages"]
    participants=list(dict.fromkeys(participants))
    return messages, participants