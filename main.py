import json
import re

FILENAME = "message.json"


def load_json():
    with open(FILENAME) as json_data:
        json_string = json.load(json_data)
    return json_string


def get_participants(json_string):
    participants = list()
    for name in json_string:
        participants.append(name['name'])
    return participants


def get_nicknames(json_string, participants):
    main_pattern = '^.*?set (his own|her own|the|your) nickname.*?$'

    nickname_patterns = {
        "someone_set_your_nickname": "^.*?set your nickname to .*?",
        "you_set_someones_nickname": "^You set the nickname for .*?",
        "someone_set_their_own_nickname": "^.*?set (his own|her own) nickname to .*?",
        "someone_set_someones_nickname": "^.*?set the nickname for .*?"
    }

    nickname_list = list()
    nickname_updates = dict()

    for message in json_string:
        try:  # Need to catch as I found that not all messages have content
            if re.match(main_pattern, message["content"]) is not None:
                nickname_list.append(message['content'])
        except:
            pass

# Make 4 lists then send them back
# 4 methods (one each) to parse seperatly

    nickname_match_a = list()
    nickname_match_b = list()
    nickname_match_c = list()
    nickname_match_d = list()

   for update in nickname_list:
        if re.match(nickname_patterns.get("someone_set_your_nickname"), update) is not None:
            nickname_updates["someone_set_your_nickname"] = update
        # elif re.match(nickname_patterns.get("you_set_someones_nickname"), update) is not None:

        # for pattern in nickname_patterns.values():
        #     if re.match(pattern, update) is not None:
        #         print (pattern, update)
    print(nickname_updates["someone_set_your_nickname"])


def main():
    json_string = load_json()
    participants = get_participants(json_string['participants'])
    get_nicknames(json_string['messages'], participants)

    # for message in json_string["messages"]:
    #     # print (message)
    #     if "set " in message['content']:
    #         print (message)


if __name__ == '__main__':
    main()
