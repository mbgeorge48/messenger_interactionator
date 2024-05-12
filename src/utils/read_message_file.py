import json


def read_message_file(*, file_to_parse, flag_message_chat_name=False):
    """
    ### input
    - file_to_parse : object
        - The contents of the messenger data
    - flag_message_chat_name : bool
        - Option to add the chat title to the message data
    ---
    ### output
    - json object containing list of participants and messages
    """
    print(
        f"reading {file_to_parse}{', flagging message data' if flag_message_chat_name else ''}"
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
