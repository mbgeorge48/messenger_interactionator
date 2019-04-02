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

    nickname_patterns = { #Need one for one's you set your self
        "someone_set_your_nickname": "^.*?set your nickname to .*?",
        "you_set_someones_nickname": "^You set the nickname for .*?",
        "someone_set_their_own_nickname": "^.*?set (his own|her own) nickname to .*?",
        "someone_set_someones_nickname": "^.*?set the nickname for .*?"
    }

    nickname_details = dict()
    for message in json_string:
        try:  # Need to catch as I found that not all messages have content
            if re.match(main_pattern, message["content"]) is not None:
                nickname_details[message['content']] = message['timestamp']
        except:
            pass

    # Matches the 4 regex patterns in "nickname_patterns"
    # https://docs.python.org/2/library/collections.html#collections.defaultdict rather than 4 lists?
    nickname_match_a = list()
    nickname_match_b = list()
    nickname_match_c = list()
    nickname_match_d = list()

    for item in list(nickname_details.items()):
        if re.match(nickname_patterns.get("someone_set_your_nickname"), item.key()) is not None:
            nickname_match_a.append(item.key())
        elif re.match(nickname_patterns.get("you_set_someones_nickname"), item) is not None:
            nickname_match_b.append(item.key())
        elif re.match(nickname_patterns.get("someone_set_their_own_nickname"), item) is not None:
            nickname_match_c.append(item.key())
        elif re.match(nickname_patterns.get("someone_set_someones_nickname"), item) is not None:
            nickname_match_d.append(item.key())

    return "None"


def main():
    json_string = load_json()
    participants = get_participants(json_string['participants'])
    all_nicknames = get_nicknames(json_string['messages'], participants)
    # once all the nicknames are returned search the values for participants
    # after that you need to pull the nickname out 


if __name__ == '__main__':
    main()
