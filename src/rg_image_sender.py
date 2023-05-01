import os
import sys

from src.utils import get_participants, load_json


def get_all_reacted_messages(json_string):
    reacted_messages = ""

    return reacted_messages


def sort_reacts(all_reacted_messages, participants):
    reacted_messages = ""
    # Sort into number of reacts in decending order
    return reacted_messages


def find_most_and_least_reactive_participant(all_reacted_messages, participants):
    return ""


def find_most_likely_to_react_with(all_reacted_messages, participants, emojis):
    return ""


def main(file_to_parse):
    json_string = load_json(file_to_parse)
    participants = get_participants(json_string["participants"])
    all_reacted_messages = sort_reacts(
        get_all_reacted_messages(json_string["messages"]), participants
    )

    # Pull of the most/least reactive person
    # Run with the common emojis (laugh(all types), shock, heart)

    # with open('react_results.json', 'w') as f:
    #     json.dump(list_of_stuff, f, indent=4, separators=(',', ': '), ensure_ascii=False)


if __name__ == "__main__":
    if os.path.isfile(sys.argv[1]):
        main(sys.argv[1])
    else:
        print("Missing path to file")
