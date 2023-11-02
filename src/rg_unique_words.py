import datetime
import json
import os
import sys

import argparse
import operator
from emoji import is_emoji, emojize

from utils import (
    get_data_to_parse,
    initial_file_load,
    initialise_counter_dict,
    write_to_file,
    encode_string,
)


def verified_word(word):
    if "http" not in word and not word.isnumeric():
        if not is_emoji(emojize(word)):
            return "".join(
                e for e in encode_string(word, emojize=True) if e.isalnum()
            ).lower()
        else:
            return word
    else:
        return None


def emoji_or_noji(word, emojis_only):
    if (
        word is not None
        and (emojis_only and is_emoji(emojize(word)))
        or emojis_only is not True
    ):
        return True
    return False


# Handle the paths not existing
def main(data_to_parse, date_range_start, date_range_end, emojis_only):
    messages, _ = get_data_to_parse(data_to_parse, date_range_start, date_range_end)
    word_data = {}

    print(
        f"Total Number of messages since {datetime.datetime.fromtimestamp(messages[0]['timestamp_ms']/1000).strftime('%Y-%m-%d %H:%M:%S')}: {len(messages)}"
    )
    for message in messages:
        try:
            for word in message["content"].split(" "):
                formatted_word = verified_word(word)
                if emoji_or_noji(formatted_word, emojis_only):
                    if formatted_word in word_data.keys():
                        word_data[formatted_word]["count"] = (
                            word_data[formatted_word]["count"] + 1
                        )
                    else:
                        word_data.update(
                            {
                                formatted_word: {
                                    "count": 1,
                                    "op": message["sender_name"],
                                }
                            }
                        )
        except KeyError:
            continue

    data = dict(sorted(word_data.items(), key=lambda item: item[1]["count"]))
    sender_count = {}
    for word in data:
        if data[word]["op"] in sender_count.keys():
            sender_count[data[word]["op"]] = sender_count[data[word]["op"]] + 1
        else:
            sender_count[data[word]["op"]] = 1
    data["sender count"] = sender_count
    write_to_file("unique_words.json", data)


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
        "--emojis", type=bool, default=False, help="Only count emojis rather than words"
    )

    args = parser.parse_args()

    main(
        initial_file_load(args.file, args.multichat),
        args.drstart,
        args.drend,
        args.emojis,
    )

# Want to be able to compare a date range to the full maximum date range
