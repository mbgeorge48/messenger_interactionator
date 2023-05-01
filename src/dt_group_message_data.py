import os
import re
import sys
from operator import itemgetter

from src.utils import encode_string, load_json
from utils import process_message_data, write_to_file


def delete_files(full_path):
    print("\tDeleting the combined message files")
    for file in os.listdir(full_path):
        if re.search("^message.*?.json$", file):
            try:
                os.remove(os.path.join(full_path, file))
                print(f"\t\tDeleted {file}")
            except Exception as e:
                print(f"\t\tFailed to delete {file} - {e}")


def main(dirs_to_group, delete_after_combining=False):
    for root, dirs, _ in os.walk(dirs_to_group, topdown=False):
        for name in dirs:
            full_path = os.path.join(root, name)
            this_groups_message_data = {}
            for file in os.listdir(full_path):
                if re.search("^message.*?.json$", file):
                    json_string = load_json(os.path.join(full_path, file))
                    if not this_groups_message_data:
                        this_groups_message_data = json_string
                    else:
                        participants_list = this_groups_message_data.get("participants")
                        for participant in json_string.get("participants"):
                            if participant not in participants_list:
                                participants_list.append(participant)
                        this_groups_message_data.update(
                            {"participants": participants_list}
                        )

                        this_groups_message_data.update(
                            {
                                "messages": this_groups_message_data["messages"]
                                + json_string["messages"]
                            }
                        )

            if this_groups_message_data:
                this_groups_message_data.update(
                    {"title": encode_string(this_groups_message_data["title"])}
                )
                for message in this_groups_message_data["messages"]:
                    message = process_message_data(message)

                this_groups_message_data.update(
                    {
                        "messages": sorted(
                            this_groups_message_data.get("messages"),
                            key=itemgetter("timestamp_ms"),
                        )
                    }
                )
                print(this_groups_message_data.get("title"))
                write_to_file("combined_messages.json", this_groups_message_data)
                if delete_after_combining:
                    delete_files(full_path)


if __name__ == "__main__":
    if os.path.isdir(sys.argv[1]):
        main(sys.argv[1], True if sys.argv[2] == "delete" else False)
    else:
        print("Missing path")
