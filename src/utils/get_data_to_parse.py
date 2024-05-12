import calendar
from datetime import datetime

import utils


def convert_string_to_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")


def date_filter(*, messages, date_range):
    latest_message = convert_string_to_date(messages[0]["timestamp_converted"])
    earliest_message = convert_string_to_date(messages[-1]["timestamp_converted"])
    date_range_start = convert_string_to_date(date_range["start"])
    date_range_end = convert_string_to_date(date_range["end"])

    if date_range_end > latest_message and date_range_start < earliest_message:
        return messages

    if date_range_start > latest_message or date_range_end < earliest_message:
        return []

    filtered_messages = []
    for message in messages:
        if date_range["start"] <= message["timestamp_converted"] <= date_range["end"]:
            filtered_messages.append(message)

    return filtered_messages


def convert_date(date_string, end_of_month=False):
    try:
        date = datetime.strptime(date_string, "%Y-%m")
    except (ValueError, TypeError):
        date = date_string
        pass

    if end_of_month:
        date = date.replace(
            day=calendar.monthrange(date.year, date.month)[1],
            hour=23,
            minute=59,
            second=59,
        )
    return date.strftime("%Y-%m-%d %H:%M:%S")


def get_data_to_parse(
    data_to_parse, date_range_start, date_range_end, flag_message_chat_name=False
):
    """
    ### input
    - data_to_parse : object
        - list of files to process
    - date_range_start : string
        - the year and month to filter the dates on
            - format = YYYY-MM
    - date_range_end : string
        - the year and month to filter the dates on
            - format = YYYY-MM
    - flag_message_chat_name : bool
        - Option to add the chat title to the message data
    ---
    ### output
    - json object containing list of participants and messages
    """
    date_range = {}
    date_range["start"] = convert_date(
        date_range_start if date_range_start else "2000-01"
    )
    date_range["end"] = convert_date(
        (date_range_end if date_range_end else datetime.today().strftime("%Y-%m")),
        True,
    )
    data = []
    for file in data_to_parse:
        data.append(
            utils.read_message_file(
                file_to_parse=file, flag_message_chat_name=flag_message_chat_name
            )
        )
    participants = messages = []
    for entry in data:
        participants = participants + utils.get_participants(
            json_string=entry["participants"]
        )
        messages = messages + date_filter(
            messages=entry["messages"], date_range=date_range
        )
    participants = list(dict.fromkeys(participants))
    return messages, participants
