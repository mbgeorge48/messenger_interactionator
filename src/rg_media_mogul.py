import operator
import sys
from operator import itemgetter

from utils import (
    get_data_to_parse,
    initial_file_load,
    initialise_counter_dict,
    write_to_file,
)


def get_all_media_sent_messages(messages):
    all_media_sent_messages = []
    for message in messages:
        if (
            message.get("photos")
            or message.get("videos")
            or message.get("files")
            or message.get("audio")
            or message.get("gifs")
        ):
            all_media_sent_messages.append(message)
    return all_media_sent_messages


def count_media_sent_by_participants(all_media_sent_messages, media_sender):
    for message in all_media_sent_messages:
        try:
            media_sender[message["sender_name"]] += 1
        except KeyError:
            media_sender[message["sender_name"]] = 0
            media_sender[message["sender_name"]] += 1
    media_sender = dict(
        sorted(media_sender.items(), key=lambda item: item[1], reverse=True)
    )
    return media_sender


def get_media_sent_by_participant_count_breakdowns(all_media_sent_messages):
    media_sent_breakdown = {}
    for message in all_media_sent_messages:
        try:
            media_sent_breakdown[message["sender_name"]]
        except KeyError:
            media_sent_breakdown[message["sender_name"]] = {
                "photos": 0,
                "videos": 0,
                "files": 0,
                "audio": 0,
                "gifs": 0,
            }

        for media_type in ["photos", "videos", "files", "audio", "gifs"]:
            if message.get(media_type):
                media_sent_breakdown[message["sender_name"]][media_type] += len(
                    message.get(media_type)
                )

    for participant in media_sent_breakdown:
        media_sent_breakdown[participant] = dict(
            sorted(
                media_sent_breakdown[participant].items(),
                key=lambda item: item[1],
                reverse=True,
            )
        )
    return media_sent_breakdown


def get_media_sent_by_type_count_breakdowns(all_media_sent_messages):
    media_sent_breakdown = {}
    for message in all_media_sent_messages:
        for media_type in ["photos", "videos", "files", "audio", "gifs"]:
            if message.get(media_type):
                try:
                    media_sent_breakdown[media_type] += len(message.get(media_type))
                except KeyError:
                    media_sent_breakdown[media_type] = 0
                    media_sent_breakdown[media_type] += len(message.get(media_type))

    media_sent_breakdown = dict(
        sorted(media_sent_breakdown.items(), key=lambda item: item[1], reverse=True)
    )
    return media_sent_breakdown


def main(data_to_parse, date_range_start, date_range_end):
    messages, participants = get_data_to_parse(
        data_to_parse, date_range_start, date_range_end
    )

    data = {}
    media_sender = initialise_counter_dict(participants)
    all_media_sent_messages = get_all_media_sent_messages(messages)
    data["media_sent_totals"] = count_media_sent_by_participants(
        all_media_sent_messages, media_sender
    )
    data[
        "media_sent_breakdowns_participant"
    ] = get_media_sent_by_participant_count_breakdowns(all_media_sent_messages)
    data["media_sent_breakdowns_media_type"] = get_media_sent_by_type_count_breakdowns(
        all_media_sent_messages
    )

    write_to_file(
        "media_mogul_results.json",
        data,
    )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        date_range_start = None
        date_range_end = None
        if len(sys.argv) > 2:
            date_range_start = sys.argv[2]
        if len(sys.argv) > 3:
            date_range_end = sys.argv[3]
        main(initial_file_load(sys.argv[1]), date_range_start, date_range_end)
    else:
        print("Missing path to file")