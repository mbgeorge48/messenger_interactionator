import datetime
import json
import os
import sys

from src.utils import encode_string, load_json

# OUTDATED


def main(file_to_parse):
    json_string = load_json(file_to_parse)
    all_messages = json_string["messages"]
    all_words = {}

    print(
        f"Total Number of messages since {datetime.datetime.fromtimestamp(all_messages[0]['timestamp_ms']/1000).strftime('%Y-%m-%d %H:%M:%S')}: {len(all_messages)}"
    )
    for index, message in enumerate(all_messages):
        print(f"On message {index} of {len(all_messages)}")
        try:
            for word in message["content"].split(" "):
                formatted_word = "".join(
                    e for e in encode_string(word) if e.isalnum()
                ).lower()
                if "http" not in formatted_word and not formatted_word.isnumeric():
                    if formatted_word in all_words.keys():
                        all_words[formatted_word] = all_words[formatted_word] + 1
                    else:
                        all_words[formatted_word] = 1
        except:
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
    if os.path.isfile(sys.argv[1]):
        main(sys.argv[1])
    else:
        print("Missing path to file")
