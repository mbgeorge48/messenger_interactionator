import datetime
import json
import os
import re
import sys

from utils import encode_string, load_json, process_message_data


def main(dirs_to_format):
    for root, dirs, _ in os.walk(dirs_to_format, topdown=False):
        for name in dirs:
            full_path = os.path.join(root, name)
            for file in os.listdir(full_path):
                if re.search("^message.*?.json$", file):
                    json_string = load_json(os.path.join(full_path,file))
                    json_string['title']=encode_string(json_string.get('title'))
                    for message in json_string['messages']:
                        message = process_message_data(message)
                    print(json_string.get('title')) # Need better logging everywhere
                    with open(os.path.join(full_path,file), 'w') as f:
                        json.dump(json_string, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    if len(sys.argv)>1:
        if os.path.isdir(sys.argv[1]):
            main(sys.argv[1])
        else:
            print('Missing path')
    else:
        print('Missing path')