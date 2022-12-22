from operator import itemgetter
import json
import os
import re
import sys

DIR="/Users/mg/Documents/FB/merged/messages/inbox"

def main(dirs_to_group):
    for root, dirs, _ in os.walk(dirs_to_group, topdown=False):
        for name in dirs:
            full_path = os.path.join(root, name)
            this_groups_message_data = {}
            for file in os.listdir(full_path):
                if re.search("^message.*?.json$", file):
                    json_file = open(os.path.join(full_path,file))
                    json_data = json.load(json_file)
                    json_file.close()
                    if not this_groups_message_data:
                        this_groups_message_data = json_data
                    else:
                        participants_list = this_groups_message_data["participants"]
                        for participant in json_data["participants"]:
                            if participant not in participants_list:
                                participants_list.append(participant)
                        this_groups_message_data.update({'participants': participants_list })

                        message_list = json_data["messages"]+this_groups_message_data["messages"]
                        sorted_messages = sorted(message_list, key=itemgetter('timestamp_ms'))
                        this_groups_message_data.update({'messages': sorted_messages })

            if this_groups_message_data:
                with open(os.path.join(full_path,'combined_messages.json'), 'w') as f:
                    json.dump(this_groups_message_data, f, indent=4)
                    print(os.path.join(full_path,'combined_messages.json'))

if __name__ == '__main__':
    if os.path.isdir(sys.argv[1]):
        main(sys.argv[1])
    else:
        print('Missing path')