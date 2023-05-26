import argparse
from datetime import datetime

from utils import get_data_to_parse, initial_file_load


def get_longest_message(messages):
    longest_message_length = 0
    longest_message = {}
    for message in messages:
        if (
            message.get("content")
            and len(message.get("content")) > longest_message_length
        ):
            longest_message_length = len(message.get("content"))
            longest_message = message
    return longest_message


def most_active(messages):
    data = {}
    for message in messages:
        try:
            data[message["sender_name"]] += 1
        except KeyError:
            data[message["sender_name"]] = 1
    return dict(sorted(data.items(), key=lambda item: item[1], reverse=True))


def get_yearly_message_count(messages):
    data = {}
    for message in messages:
        year = int(
            datetime.strptime(
                message.get("timestamp_converted"), "%Y-%m-%d %H:%M:%S"
            ).strftime("%Y")
        )
        try:
            data[year] += 1
        except KeyError:
            data[year] = 1
    return data


def get_average_messages_a_day(messages):
    data = {}
    days_messages = [messages[0]]
    for message in messages:
        day = datetime.strptime(
            days_messages[0].get("timestamp_converted"), "%Y-%m-%d %H:%M:%S"
        ).strftime("%Y-%m-%d")
        if (
            datetime.strptime(
                message.get("timestamp_converted"), "%Y-%m-%d %H:%M:%S"
            ).strftime("%Y-%m-%d")
            == day
        ):
            days_messages.append(message)
        else:
            data[day] = len(days_messages)
            days_messages = [message]

    average_messages = len(messages) / len(data.values())
    return average_messages


def get_busiest_weekday(messages):
    # Monday is 0 and Sunday is 6
    data = {}
    for message in messages:
        day = int(
            datetime.strptime(
                message.get("timestamp_converted"), "%Y-%m-%d %H:%M:%S"
            ).weekday()
        )
        try:
            data[day] += 1
        except KeyError:
            data[day] = 1
    return data


def main(data_to_parse, date_range_start, date_range_end, function):
    messages, _ = get_data_to_parse(data_to_parse, date_range_start, date_range_end)

    if function == "longest-message":
        longest_message = get_longest_message(messages)
        print(longest_message, len(longest_message.get("content").split()))
    if function == "most-active":
        participant_message_count = most_active(messages)
        print(participant_message_count)
    if function == "yearly-message-count":
        yearly_message_count = get_yearly_message_count(messages)
        print(yearly_message_count)
    if function == "average-messages":
        average_messages = get_average_messages_a_day(messages)
        print(average_messages)
    if function == "busiest-day":
        busiest_day = get_busiest_weekday(messages)
        print(busiest_day)


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
        "-func",
        "--function",
        type=str,
        required=True,
        choices=[
            "longest-message",
            "most-active",
            "yearly-message-count",
            "average-messages",
            "busiest-day",
        ],
    )

    args = parser.parse_args()

    main(
        initial_file_load(args.file, args.multichat),
        args.drstart,
        args.drend,
        args.function,
    )
