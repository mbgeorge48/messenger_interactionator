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
                        participants_list = this_groups_message_data["participants"]
                        for participant in json_string["participants"]:
                            if participant not in participants_list:
                                participants_list.append(participant)
                        this_groups_message_data.update({'participants': participants_list })

                        this_groups_message_data.update({'messages': this_groups_message_data["messages"].extend(json_string["messages"]) })


            if this_groups_message_data:
                this_groups_message_data.update({'title':encode_string(this_groups_message_data['title'])})
                for message in this_groups_message_data['messages']:
                    try:
                        message['content'] = encode_string(message['content'])
                    except:
                        continue
                this_groups_message_data.update({'messages': sorted(this_groups_message_data['messages'], key=itemgetter('timestamp_ms')) })

                with open(os.path.join(full_path,'combined_messages.json'), 'w') as f:
                    json.dump(this_groups_message_data, f, indent=4, ensure_ascii=False)
                    print(os.path.join(full_path,'combined_messages.json'))

if __name__ == '__main__':
    if os.path.isdir(sys.argv[1]):
        main(sys.argv[1])
    else:
        print('Missing path')