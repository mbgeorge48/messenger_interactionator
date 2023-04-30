import json
import re
import collections
import datetime
import sys
import os

from utils.utils import load_json


def main(dir_to_scan, media_type, print_logs, all_child_dirs):
    if all_child_dirs:
        for folder in os.listdir(dir_to_scan):
            path=os.path.join(dir_to_scan, folder)
            print(path)
            if os.path.isdir(path):
                process_folder(path, media_type, print_logs)
    else:
        process_folder(dir_to_scan, media_type, print_logs)



def process_folder(path, media_type, print_logs):
    media_path = os.path.join(path, media_type)
    if os.path.exists(media_path):
        media_files = os.listdir(media_path)
    else:
        print(f"{media_type} folder not found - {path}")
        return None
    messages_path = os.path.join(path, "combined_messages.json")
    json_string = load_json(messages_path)
    messages = json_string["messages"]

    updated_messages = []
    for message in messages:
        if message.get(media_type):
            for media_index, media in enumerate(message.get(media_type)):
                file = (os.path.split(media.get('uri'))[1])
                if file in media_files:
                    if print_logs:
                        print(file,)
                    _, file_extension = os.path.splitext(file)
                    media_timestamp = datetime.datetime.fromtimestamp(message['timestamp_ms']/1000).strftime('%Y-%m-%d_%H%M%S')
                    media_sender = message['sender_name'].replace(' ', '_')
                    new_name = f"{media_timestamp}-{media_sender}{file_extension}"

                    current_path = os.path.join(path, media_type, file)
                    new_path = os.path.join(path, media_type, new_name)

                    print(f'Renaming {current_path} to {new_path}', end="")
                    try:
                        os.rename(current_path, new_path)
                        message.get(media_type)[media_index]['uri']=os.path.join(media_type, new_name)
                        updated_messages.append(message)
                    except FileNotFoundError as fnf_e:
                        print(f"\nFailed to move {file} to {new_path}", fnf_e)
                    except Exception as e:
                        print("Something went wrong", e)
        else:
            updated_messages.append(message)

    json_string.update({'messages': updated_messages})
    print('')

    with open(messages_path, 'w') as f:
        json.dump(json_string, f, indent=4, ensure_ascii=False)

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
