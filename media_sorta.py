import json
import re
import collections
import datetime
import sys
import os

from utils import load_json


def main(dir_to_scan, media_type, print_logs, all_child_dirs):
    if all_child_dirs:
        for root, dirs, _ in os.walk(dir_to_scan, topdown=False):
            for folder in dirs:
                print(folder)
                path=os.path.join(root, folder)
                process_folder(path, media_type, print_logs)
    else:
        process_folder(dir_to_scan, media_type, print_logs)



def process_folder(path, media_type, print_logs):
    messages_path = os.path.join(path, "combined_messages.json")
    json_string = load_json(messages_path)
    messages = json_string["messages"]

    media_path = os.path.join(path, media_type)
    media_files = os.listdir(media_path)

    updated_messages = []
    for message in messages:
        if message.get(media_type):
            for media_index, media in enumerate(message.get(media_type)):
                file = (os.path.split(media.get('uri'))[1])
                if file in media_files:
                    if print_logs:
                        print(file,)
                    _, file_extension = os.path.splitext(file)
                    new_name = f"{datetime.datetime.fromtimestamp(message['timestamp_ms']/1000).strftime('%Y-%m-%d_%H%M%S')}-{message['sender_name'].replace(' ', '_')}{file_extension}"
                    os.rename(os.path.join(path, media_type, file), os.path.join(path, media_type, new_name))
                    message.get(media_type)[media_index]['uri']=os.path.join(media_type, new_name)
                    updated_messages.append(message)
        else:
            updated_messages.append(message)

    json_string.update({'messages': updated_messages})

    with open(messages_path, 'w') as f:
        json.dump(json_string, f, indent=4, ensure_ascii=False)
        print(messages_path)

if __name__ == '__main__':
    if os.path.isdir(sys.argv[1]):
        for media_type in ['photos', 'videos', 'files', 'audio', 'gifs']:
            print(media_type)
            main(
                sys.argv[1],
                media_type,
                print_logs = False if '-q' in sys.argv else True,
                all_child_dirs= True if '-a' in sys.argv else False
            )
    else:
        print('Missing path to dir')
