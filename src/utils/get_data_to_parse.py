import calendar
from datetime import datetime

import utils


def convert_string_to_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")


def date_filter(messages, date_range):
    latest_message = convert_string_to_date(messages[0]["timestamp_converted"])
    earliest_message = convert_string_to_date(messages[-1]["timestamp_converted"])
    date_range_start = convert_string_to_date(date_range["start"])
    date_range_end = convert_string_to_date(date_range["end"])

    if latest_message > date_range_end and earliest_message < date_range_start:
        return messages
    elif (
        not latest_message > date_range_start and not earliest_message < date_range_end
    ):
        return []

    filtered_messages = []
    for message in messages:
        if date_range["start"] <= message["timestamp_converted"] <= date_range["end"]:
            filtered_messages.append(message)

    return filtered_messages


def convert_date(date_string, end_of_month=False):
    try:
        date = datetime.strptime(date_string, "%Y-%m")
    except ValueError:
        date = date_string

    if end_of_month:
        date = date.replace(
            day=calendar.monthrange(date.year, date.month)[1],
            hour=23,
            minute=59,
            second=59,
        )
    return date.strftime("%Y-%m-%d %H:%M:%S")


def get_data_to_parse(data_to_parse, date_range_start, date_range_end):
    date_range = {}
    date_range["start"] = convert_date(
        date_range_start if date_range_start else "2000-01"
    )
    date_range["end"] = convert_date(
        date_range_end if date_range_end else datetime.today().strftime("%Y-%m"),
        True,
    )
    print(date_range)
    data = []
    for file in data_to_parse:
        data.append(utils.read_message_file(file))
    participants = messages = []
    for entry in data:
        participants = participants + utils.get_participants(entry["participants"])
        messages = messages + date_filter(entry["messages"], date_range)
    participants = list(dict.fromkeys(participants))
    return messages, participants
