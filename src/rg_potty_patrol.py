import argparse

from utils import (get_data_to_parse, initial_file_load,
                   initialise_counter_dict, load_json, write_to_file)


def get_all_naughty_messages(messages, potty_words, potty_mouth_counter):
    partipant_specific_count = {}
    for message in messages:
        try:
            partipant_specific_count[message["sender_name"]]
        except KeyError:
            partipant_specific_count[message["sender_name"]] = {}
        if not message.get("content"):
            continue
        for potty_word in potty_words:
            if potty_word in message.get("content").lower():
                try:
                    potty_mouth_counter[message["sender_name"]] += 1
                except KeyError:
                    potty_mouth_counter[message["sender_name"]] = 0
                    potty_mouth_counter[message["sender_name"]] += 1

                try:
                    partipant_specific_count[message["sender_name"]][potty_word] += 1
                except KeyError:
                    partipant_specific_count[message["sender_name"]][potty_word] = 0
                    partipant_specific_count[message["sender_name"]][potty_word] += 1

    for participant in partipant_specific_count:
        partipant_specific_count[participant] = dict(
            sorted(
                partipant_specific_count[participant].items(),
                key=lambda item: item[1],
                reverse=True,
            )
        )

    return partipant_specific_count, potty_mouth_counter


def main(
    data_to_parse,
    date_range_start,
    date_range_end,
    potty_file,
):
    messages, participants = get_data_to_parse(
        data_to_parse, date_range_start, date_range_end
    )
    potty_words = load_json(potty_file)

    data = {}
    potty_mouth_counter = initialise_counter_dict(participants)
    partipant_specific_count, potty_mouth_counter = get_all_naughty_messages(
        messages, potty_words, potty_mouth_counter
    )
    data["partipant_specific_count"] = partipant_specific_count
    data["potty_mouth_counter"] = potty_mouth_counter

    write_to_file(
        "potty_patrol_results.json",
        data,
    )


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
    parser.add_argument(
        "--pottyfile",
        type=str,
        help="list of naughty words to look out for (json)",
        default="potty_words.json",
    )

    args = parser.parse_args()

    main(
        initial_file_load(args.file, args.multichat),
        args.drstart,
        args.drend,
        args.pottyfile,
    )
