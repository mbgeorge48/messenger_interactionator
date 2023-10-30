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


# Handle the paths not existing
def main(data_to_parse, date_range_start, date_range_end, emojis_only):
    messages, _ = get_data_to_parse(data_to_parse, date_range_start, date_range_end)
    all_words = {}

    print(
        f"Total Number of messages since {datetime.datetime.fromtimestamp(messages[0]['timestamp_ms']/1000).strftime('%Y-%m-%d %H:%M:%S')}: {len(messages)}"
    )
    for message in messages:
        try:
            for word in message["content"].split(" "):
                word_is_emoji = is_emoji(emojize(word))
                if not word_is_emoji:
                    formatted_word = "".join(
                        e for e in encode_string(word, emojize=True) if e.isalnum()
                    ).lower()
                else:
                    formatted_word = word
                if "http" not in formatted_word and not formatted_word.isnumeric():
                    if (emojis_only and word_is_emoji) or emojis_only is not True:
                        if formatted_word in all_words.keys():
                            all_words[formatted_word] = all_words[formatted_word] + 1
                        else:
                            all_words[formatted_word] = 1
        except Exception:
            continue
    alphabetical_order = dict(
        sorted(all_words.items(), key=lambda item: item[0], reverse=True)
    )
    print(
        json.dumps(
            dict(
                sorted(
                    alphabetical_order.items(), key=lambda item: item[1], reverse=True
                )
            ),
            indent=4,
            separators=(",", ": "),
            ensure_ascii=False,
        )
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
    parser.add_argument("--emojis", type=bool, default=False)

    args = parser.parse_args()

    main(
        initial_file_load(args.file, args.multichat),
        args.drstart,
        args.drend,
        args.emojis,
    )
