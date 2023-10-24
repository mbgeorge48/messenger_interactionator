import argparse
import collections
import datetime
import re

from utils import (get_data_to_parse, get_your_name, initial_file_load,
                   initialise_counter_dict, write_to_file)

YOUR_NAME = get_your_name()


def get_nicknames(json_string, nicknames_set):
    main_pattern = "^.*?set (his own|her own|the|your) nickname.*?$"
    nickname_patterns = {
        "someone_set_your_nickname": "^.*?set your nickname to .*?",
        "you_set_someones_nickname": "^You set the nickname for .*?",
        "someone_set_their_own_nickname": "^.*?set (his own|her own) nickname to .*?",
        "someone_set_someones_nickname": "^.*?set the nickname for .*?",
        "you_set_your_own_nickname": "^You set your nickname to .*?",
    }

    nickname_details = {}
    for message in json_string:
        try:  # Need to catch as I found that not all messages have content
            if re.match(main_pattern, message["content"]) is not None:
                nickname_details[message["timestamp_ms"]] = message["content"]
                nicknames_set[message["sender_name"]] += 1
        except:
            pass

    nicknames_sorted = collections.defaultdict(list)
    for item in list(nickname_details.items()):
        if (
            re.match(nickname_patterns.get("someone_set_your_nickname"), item[1])
            is not None
        ):
            nicknames_sorted["someone_set_your_nickname"].append(item)
        elif (
            re.match(nickname_patterns.get("you_set_someones_nickname"), item[1])
            is not None
        ):
            nicknames_sorted["you_set_someones_nickname"].append(item)
        elif (
            re.match(nickname_patterns.get("someone_set_their_own_nickname"), item[1])
            is not None
        ):
            nicknames_sorted["someone_set_their_own_nickname"].append(item)
        elif (
            re.match(nickname_patterns.get("someone_set_someones_nickname"), item[1])
            is not None
        ):
            nicknames_sorted["someone_set_someones_nickname"].append(item)
        elif (
            re.match(nickname_patterns.get("you_set_your_own_nickname"), item[1])
            is not None
        ):
            nicknames_sorted["you_set_your_own_nickname"].append(item)

    return nicknames_sorted, nicknames_set


def sort_nicknames(all_nicknames, participants):
    peoples_nicknames = collections.defaultdict(list)
    nickname_regex = "^.*?set.*?nickname.*?to "

    for key in all_nicknames.keys():
        for item in all_nicknames[key]:
            this_set = {
                "nickname": (re.sub(nickname_regex, "", item[1]).rstrip(".")),
                "timestamp": (
                    datetime.datetime.fromtimestamp(item[0] / 1000).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                ),
            }
            for participant in participants:
                if participant in item[1]:
                    peoples_nicknames[participant].append(this_set)
            if "someone_set_your_nickname" == key:
                peoples_nicknames[YOUR_NAME].append(this_set)
            if "you_set_your_own_nickname" == key:
                peoples_nicknames[YOUR_NAME].append(this_set)

    for participant in participants:
        peoples_nicknames[participant].sort(key=lambda x: x["timestamp"], reverse=True)

    return peoples_nicknames


def get_the_oldest_nickname(peoples_nicknames, length=3):
    current_nicknames = []
    for participant in peoples_nicknames:
        if len(peoples_nicknames[participant]) > 0:
            current_nicknames.append(
                {
                    "participant": participant,
                    "nickname": peoples_nicknames[participant][0]["nickname"],
                    "timestamp": peoples_nicknames[participant][0]["timestamp"],
                }
            )
    current_nicknames.sort(key=lambda x: x["timestamp"])

    return current_nicknames[:length]


def main(data_to_parse, date_range_start, date_range_end):
    messages, participants = get_data_to_parse(
        data_to_parse, date_range_start, date_range_end
    )
    nicknames_set = initialise_counter_dict(participants)

    all_nicknames, nicknames_set = get_nicknames(messages, nicknames_set)
    peoples_nicknames = sort_nicknames(all_nicknames, participants)
    oldest_nicknames = get_the_oldest_nickname(peoples_nicknames)

    nicknames_had = {}
    for participant in peoples_nicknames.keys():
        nicknames_had[participant] = len(peoples_nicknames[participant])
    peoples_nicknames["nicknames_had"] = dict(
        sorted(nicknames_had.items(), key=lambda item: item[1], reverse=True)
    )
    peoples_nicknames["nicknames_set"] = dict(
        sorted(nicknames_set.items(), key=lambda item: item[1], reverse=True)
    )
    peoples_nicknames["oldest_nicknames"] = oldest_nicknames

    write_to_file("nickname_results.json", peoples_nicknames)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, required=True)
    parser.add_argument("--multichat", type=bool, default=False)
    parser.add_argument(
        "--drstart",
        type=str,
        help="The date range start for getting messages, format needs to be (YYYY-MM)",
    )
    parser.add_argument(
        "--drend",
        type=str,
        help="The date range end for getting messages, format needs to be (YYYY-MM)",
    )
    args = parser.parse_args()

    main(
        initial_file_load(args.file, args.multichat),
        args.drstart,
        args.drend,
    )
