import json
import re
import collections
import datetime
import sys
import os

from utils import load_json

def main(file_to_parse):
    json_string = load_json(file_to_parse)
    photo_messages = []
    for message in json_string["messages"]:
        try:

            photo_messages.append({message['sender_name']: message['photos']})
        except:
            continue
    print(json.dumps(photo_messages, indent=4, separators=(',', ': '), sort_keys=True, ensure_ascii=False))


if __name__ == '__main__':
    if os.path.isfile(sys.argv[1]):
        main(sys.argv[1])
    else:
        print('Missing path to file')
