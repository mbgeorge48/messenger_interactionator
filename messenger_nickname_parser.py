import json
import re
import collections
import datetime
import sys
import os

YOUR_NAME = "Matt George"

def load_json(file_to_parse):
    with open(file_to_parse) as json_data:
        json_string = json.load(json_data)
    return json_string


def get_participants(json_string):
    participants = list()
    for name in json_string:
        participants.append(name['name'])
    return participants


def get_nicknames(json_string, participants):
    main_pattern = '^.*?set (his own|her own|the|your) nickname.*?$'
    nickname_patterns = {  # Need one for one's you set for yourself
        "someone_set_your_nickname": "^.*?set your nickname to .*?",
        "you_set_someones_nickname": "^You set the nickname for .*?",
        "someone_set_their_own_nickname": "^.*?set (his own|her own) nickname to .*?",
        "someone_set_someones_nickname": "^.*?set the nickname for .*?",
        "you_set_your_own_nickname": "^You set your nickname to .*?"
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
        elif re.match(nickname_patterns.get("you_set_your_own_nickname"), item[1]) is not None:
            nicknames_sorted["you_set_your_own_nickname"].append(item)

    return nicknames_sorted

def sort_nicknames(all_nicknames, participants):
    peoples_nicknames = collections.defaultdict(list)
    nickname_regex = "^.*?set.*?nickname.*?to "

    for key in all_nicknames.keys():
        for item in (all_nicknames[key]):
            this_set = {
                "nickname": (re.sub(nickname_regex, "", item[1].encode('latin1').decode('utf8')).rstrip('.')),
                "timestamp":(datetime.datetime.fromtimestamp(item[0]/1000).strftime('%Y-%m-%d %H:%M:%S'))
            }
            for person in participants:
                if person in item[1]:
                    peoples_nicknames[person].append(this_set)
            if "someone_set_your_nickname" == key:
                peoples_nicknames[YOUR_NAME].append(this_set)
            if "you_set_your_own_nickname" == key:
                peoples_nicknames[YOUR_NAME].append(this_set)

    return peoples_nicknames


def main(file_to_parse):
    json_string = load_json(file_to_parse)
    participants = get_participants(json_string['participants'])
    all_nicknames = get_nicknames(json_string['messages'], participants)

    peoples_nicknames = sort_nicknames(all_nicknames, participants)

    totals = {}
    for participant in peoples_nicknames.keys():
        print(participant,len(peoples_nicknames[participant]))
        totals[participant] = len(peoples_nicknames[participant])
    peoples_nicknames['totals'] = totals

    with open('result.json', 'w') as f:
        json.dump(peoples_nicknames, f, indent=4, separators=(',', ': '), sort_keys=True, ensure_ascii=False)


if __name__ == '__main__':
    if os.path.isfile(sys.argv[1]):
        main(sys.argv[1])
    else:
        print('Missing path to file')
