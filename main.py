import json
import re
import collections

FILENAME = "message.json"
YOURNAME = "Matt George"


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
    nickname_patterns = {  # Need one for one's you set yourself
        "someone_set_your_nickname": "^.*?set your nickname to .*?",
        "you_set_someones_nickname": "^You set the nickname for .*?",
        "someone_set_their_own_nickname": "^.*?set (his own|her own) nickname to .*?",
        "someone_set_someones_nickname": "^.*?set the nickname for .*?"
    }

    nickname_details = dict()
    for message in json_string:
        try:  # Need to catch as I found that not all messages have content
            if re.match(main_pattern, message["content"]) is not None:
                nickname_details[message['timestamp_ms']] = message['content']
        except:
            pass

    nicknames_sorted = collections.defaultdict(list)

    for item in list(nickname_details.items()):
        if re.match(nickname_patterns.get("someone_set_your_nickname"), item[1]) is not None:
            nicknames_sorted["someone_set_your_nickname"].append(item)
        elif re.match(nickname_patterns.get("you_set_someones_nickname"), item[1]) is not None:
            nicknames_sorted["you_set_someones_nickname"].append(item)
        elif re.match(nickname_patterns.get("someone_set_their_own_nickname"), item[1]) is not None:
            nicknames_sorted["someone_set_their_own_nickname"].append(item)
        elif re.match(nickname_patterns.get("someone_set_someones_nickname"), item[1]) is not None:
            nicknames_sorted["someone_set_someones_nickname"].append(item)

    return nicknames_sorted


def main():
    json_string = load_json()
    participants = get_participants(json_string['participants'])
    all_nicknames = get_nicknames(json_string['messages'], participants)

    peoples_nicknames = collections.defaultdict(list)
    nickname_regex = "^.*?set.*?nickname.*?to "

    # Not idea code but will clean up later

    for item in (all_nicknames["you_set_someones_nickname"]):
        nickname = re.sub(nickname_regex, "", item[1])
        for person in participants:
            if person in item[1]:
                peoples_nicknames[person].append(nickname)

    for item in (all_nicknames["someone_set_their_own_nickname"]):
        nickname = re.sub(nickname_regex, "", item[1])
        for person in participants:
            if person in item[1]:
                peoples_nicknames[person].append(nickname)

    for item in (all_nicknames["someone_set_someones_nickname"]):
        nickname = re.sub(nickname_regex, "", item[1])
        for person in participants:
            if person in item[1]:
                peoples_nicknames[person].append(nickname)

    for item in (all_nicknames["someone_set_your_nickname"]):
        nickname = re.sub(nickname_regex, "", item[1])
        peoples_nicknames[YOURNAME].append(nickname)

    print(peoples_nicknames[participants[1]])


if __name__ == '__main__':
    main()
