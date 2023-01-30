import datetime
from operator import itemgetter
import json
import os
import re
import sys

from utils import encode_string, load_json

def main(dirs_to_group):
    for root, dirs, _ in os.walk(dirs_to_group, topdown=False):
        for name in dirs:
            full_path = os.path.join(root, name)
            this_groups_message_data = {}
            for file in os.listdir(full_path):
                if re.search("^message.*?.json$", file):
                    json_string = load_json(os.path.join(full_path,file))
                    if not this_groups_message_data:
                        this_groups_message_data = json_string
                    else:
                        participants_list = this_groups_message_data.get("participants")
                        for participant in json_string.get("participants"):
                            if participant not in participants_list:
                                participants_list.append(participant)
                        this_groups_message_data.update({'participants': participants_list })

                        this_groups_message_data.update({'messages': this_groups_message_data["messages"]+json_string["messages"] })


            if this_groups_message_data:
                this_groups_message_data.update({'title':encode_string(this_groups_message_data['title'])})
                for message in this_groups_message_data['messages']:

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

                this_groups_message_data.update({'messages': sorted(this_groups_message_data.get('messages'), key=itemgetter('timestamp_ms')) })
                print(this_groups_message_data.get('title'))
                with open(os.path.join(full_path,'combined_messages.json'), 'w') as f:
                    json.dump(this_groups_message_data, f, indent=4, ensure_ascii=False)
                print('\tDeleting the combined message files')
                for file in os.listdir(full_path):
                    if re.search("^message.*?.json$", file):
                        try:
                            os.remove(os.path.join(full_path, file))
                            print(f'\t\tDeleted {file}')
                        except Exception as e:
                            print(f'\t\tFailed to delete {file} - {e}')

if __name__ == '__main__':
    if os.path.isdir(sys.argv[1]):
        main(sys.argv[1])
    else:
        print('Missing path')