import json


def read_message_file(file_to_parse, flag_message_chat_name=False):
    print(
        f"reading {file_to_parse}, {'flagging message data' if flag_message_chat_name else None}"
    )
    with open(file_to_parse) as json_data:
        json_string = json.load(json_data)
    payload = {
        "messages": json_string["messages"],
        "participants": json_string["participants"],
    }
    if flag_message_chat_name:
        chat_name = json_string["title"]
        for message in payload["messages"]:
            message["chat_name"] = chat_name

    return payload
