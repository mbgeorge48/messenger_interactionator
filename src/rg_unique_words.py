#!/usr/bin/env python
# Add notes to readme
# brew install enchant
# GL windows, maybe a docker container?
# export PYENCHANT_LIBRARY_PATH=/opt/homebrew/lib/libenchant-2.dylib

import argparse
import datetime
from emoji import emojize, is_emoji
from utils import (
    encode_string,
    get_data_to_parse,
    initial_file_load,
    write_to_file,
)
from string import punctuation
import enchant

d = enchant.Dict("en_GB")

invalid_words = []


def verified_word(word):
    # Check for http in word
    if "http" in word:
        invalid_words.append(word)
        return None
    # Check if the word is numeric
    if word.isnumeric():
        invalid_words.append(word)
        return None
    # Check if the word is an emoji
    if is_emoji(emojize(word)):
        invalid_words.append(word)
        return None

    # Check if the word without punctuation still has a value
    if len(word.strip(punctuation)) > 0:
        # Check if the word is valid according to pyenchant
        if not d.check(word.strip(punctuation)):
            invalid_words.append(word)
            return None

    cleaned_word = "".join(
        e for e in encode_string(word, emojize=True) if e.isalnum()
    ).lower()
    return cleaned_word


def emoji_or_noji(word, emojis_only):
    if word is None:
        return False
    if emojis_only is not True:
        return True
    if is_emoji(emojize(word)):
        return True
    return False


def list_every_word(all_messages, emojis_only):
    all_words = set()
    for message in all_messages:
        try:
            content = message.get("content", "")
            words = content.split(" ")

            for word in words:
                formatted_word = verified_word(word)
                if emoji_or_noji(formatted_word, emojis_only):
                    all_words.add(formatted_word)
        except KeyError:
            continue

    return list(all_words)


# Handle the paths not existing
def main(data_to_parse, date_range_start, date_range_end, emojis_only, compare_year):
    all_previous_years_words = set()

    if compare_year:
        today = datetime.now()
        messages, _ = get_data_to_parse(
            data_to_parse, "-".join([str(today.year), "01"]), None
        )
        all_messages, _ = get_data_to_parse(
            data_to_parse,
            None,
            "-".join([str(today.year - 1), "12"]),
        )
        all_previous_years_words = list_every_word(all_messages, emojis_only)

    else:
        messages, _ = get_data_to_parse(data_to_parse, date_range_start, date_range_end)

    word_data = {}
    sender_count = {}

    messages.reverse()
    for message in messages:
        try:
            words = message.get("content", "").split(" ")
            sender_name = message.get("sender_name", "")
            for word in words:
                formatted_word = verified_word(word)

                if (
                    emoji_or_noji(formatted_word, emojis_only)
                    and formatted_word not in all_previous_years_words
                ):
                    if formatted_word in word_data.keys():
                        word_data[formatted_word]["count"] += 1
                    else:
                        word_data[formatted_word] = {
                            "count": 1,
                            "op": sender_name,
                        }
                        sender_count[sender_name] = sender_count.get(sender_name, 0) + 1
        except KeyError:
            continue

    sorted_word_data = dict(
        sorted(word_data.items(), key=lambda item: item[1]["count"])
    )
    sorted_sender_count = dict(sorted(sender_count.items(), key=lambda item: item[1]))

    sorted_word_data["sender_count"] = sorted_sender_count
    sorted_word_data["invalid_words"] = sorted(list(dict.fromkeys(invalid_words)))

    write_to_file("unique_words.json", sorted_word_data)


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
    parser.add_argument(
        "--compareyear",
        type=bool,
        default=False,
        help="Compare the current year to the previous years",
    )

    args = parser.parse_args()

    main(
        initial_file_load(args.file, args.multichat),
        args.drstart,
        args.drend,
        args.emojis,
        args.compareyear,
    )

# Want to be able to compare a date range to the full maximum date range
