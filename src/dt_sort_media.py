import argparse
import datetime
import json
import os
import sys

from utils import get_data_to_parse, initial_file_load, load_json, write_to_file


def update_media(message, media_object, media_index, media_file, path):
    _, file_extension = os.path.splitext(media_file)
    media_timestamp = datetime.datetime.fromtimestamp(
        message["timestamp_ms"] / 1000
    ).strftime("%Y-%m-%d_%H%M%S")
    media_sender = message["sender_name"].replace(" ", "_")
    new_name = f"{media_timestamp}-{media_sender}{file_extension}"

    current_path = os.path.join(path, media_type, media_file)
    new_path = os.path.join(path, media_type, new_name)

    print(f"Renaming {current_path} to {new_path}", end="")
    try:
        os.rename(current_path, new_path)
        message.get(media_type)[media_index]["uri"] = os.path.join(media_type, new_name)
    except FileNotFoundError as fnf_e:
        print(f"\nFailed to move {media_file} to {new_path}", fnf_e)
    except Exception as e:
        print("Something unexpected went wrong", e)

    return message


def sort_media(file, media_files, media_type, path, print_logs):
    json_string = load_json(file)
    messages = json_string.get("messages")

    updated_messages = []
    for message in messages:
        if not message.get(media_type):
            updated_messages.append(message)
            continue

        for media_index, media_object in enumerate(message.get(media_type)):
            file = os.path.split(media_object.get("uri"))[1]
            if file in media_files:
                message = update_media(message, media_object, media_index, file, path)
                if print_logs:
                    print(
                        file,
                    )

    json_string.update({"messages": updated_messages})
    print("")

    write_to_file(file, json_string)


def process_folder(path, media_type, print_logs):
    media_path = os.path.join(path, media_type)
    if not os.path.exists(media_path):
        print(f"{media_type} folder not found - {path}")
        return None
    else:
        media_files = os.listdir(media_path)

    files_to_update = initial_file_load(path)

    for file in files_to_update:
        sort_media(file, media_files, media_type, path, print_logs)

    # messages, _ = get_data_to_parse(files_to_update)


def main(dir_to_scan, print_logs, all_child_dirs, media_type):
    if not all_child_dirs:
        process_folder(dir_to_scan, media_type, print_logs)
    else:
        for folder in os.listdir(dir_to_scan):
            path = os.path.join(dir_to_scan, folder)
            print(path)
            if os.path.isdir(path):
                process_folder(path, media_type, print_logs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", type=str, required=True)
    parser.add_argument("-q", "--quiet", type=bool)
    parser.add_argument("-c", "--childdirs", type=bool)
    parser.add_argument(
        "-sm",
        "--mediatype",
        type=str,
        choices=["photos", "videos", "files", "audio", "gifs"],
    )

    args = parser.parse_args()
    for media_type in (
        [args.mediatype]
        if args.mediatype
        else ["photos", "videos", "files", "audio", "gifs"]
    ):
        main(args.dir, args.quiet, args.childdirs, media_type)
