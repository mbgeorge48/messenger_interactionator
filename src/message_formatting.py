import datetime
import json
import os
import re
import sys

from utils import encode_string, load_json


def main(dirs_to_group):
    for root, dirs, _ in os.walk(dirs_to_group, topdown=False):
        for name in dirs:
            full_path = os.path.join(root, name)
            for file in os.listdir(full_path):
                if re.search("^message.*?.json$", file):
                    json_string = load_json(os.path.join(full_path,file))
                    json_string['title']=encode_string(json_string.get('title'))
                    for message in json_string['messages']:
                        if message.get("content"):
                            message['content'] = encode_string(message.get('content'))
                        if message.get("bumped_message_metadata") and message.get("bumped_message_metadata").get("bumped_message") :
                            message["bumped_message_metadata"]["bumped_message"] = encode_string(message.get('bumped_message_metadata').get("bumped_message"))
                        if message.get("reactions"):
                            for reaction in message.get("reactions"):
                                reaction["reaction"] = encode_string(reaction.get('reaction'))
                        if message.get("audio_files"):
                            message["audio"] = message.pop("audio_files")
                        message["timestamp_converted"] = datetime.datetime.fromtimestamp(message['timestamp_ms']/1000).strftime('%Y-%m-%d %H:%M:%S')
                    print(json_string.get('title'))
                    with open(os.path.join(full_path,file), 'w') as f:
                        json.dump(json_string, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    if os.path.isdir(sys.argv[1]):
        main(sys.argv[1])
    else:
        print('Missing path')