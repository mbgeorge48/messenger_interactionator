#!/usr/bin/env python

import argparse
import operator

from utils import (
    get_data_to_parse,
    initial_file_load,
    initialise_counter_dict,
    write_to_file,
)


def get_all_reacted_messages(messages, min_reactions_length=0):
    all_reacted_messages = []
    for message in messages:
        if len(message.get("reactions", [])) > min_reactions_length:
            message["reactions_length"] = len(message["reactions"])
            all_reacted_messages.append(message)
    sorted_all_reacted_messages = sorted(
        all_reacted_messages, key=operator.itemgetter("reactions_length"), reverse=True
    )
    return sorted_all_reacted_messages


def find_most_and_least_reactive_participant(all_reacted_messages, participants):
    times_reacted = {participant: 0 for participant in participants}
    for message in all_reacted_messages:
        for reaction in message.get("reactions", []):
            actor = reaction["actor"]
            if actor in participants:
                times_reacted[actor] += 1

    times_reacted = dict(
        sorted(times_reacted.items(), key=lambda item: item[1], reverse=True)
    )
    return times_reacted


def find_most_likely_to_react_with(all_reacted_messages, emojis, reaction_counter):
    for message in all_reacted_messages:
        for reaction in message.get("reactions", []):
            if reaction["reaction"] in emojis:
                actor = reaction["actor"]
                reaction_counter[actor] = reaction_counter.get(actor, 0) + 1

    sorted_reaction_counter = dict(
        sorted(reaction_counter.items(), key=lambda item: item[1], reverse=True)
    )
    return sorted_reaction_counter


def find_most_common_reaction(all_reacted_messages):
    emoji_counter = {}

    for message in all_reacted_messages:
        for reaction in message.get("reactions", []):
            emoji = reaction["reaction"]
            emoji_counter[emoji] = emoji_counter.get(emoji, 0) + 1

    sorted_emoji_counter = dict(
        sorted(emoji_counter.items(), key=lambda item: item[1], reverse=True)
    )
    return sorted_emoji_counter


def find_each_participants_biggest_fan(all_reacted_messages):
    fan_zone = {}
    for message in all_reacted_messages:
        sender_name = message["sender_name"]
        fan_zone.setdefault(sender_name, {})

        for reaction in message.get("reactions", []):
            actor = reaction["actor"]
            fan_zone[sender_name][actor] = fan_zone[sender_name].get(actor, 0) + 1

    for participant in fan_zone:
        fan_zone[participant] = dict(
            sorted(
                fan_zone[participant].items(), key=lambda item: item[1], reverse=True
            )
        )
    return fan_zone


def get_emjois_to_search(emojis_key):
    if emojis_key == "laugh":
        return [
            ":grinning_squinting_face:",
            ":grinning_face_with_sweat:",
            ":rolling_on_the_floor_laughing:",
            ":face_with_tears_of_joy:",
        ]
    if emojis_key == "heart":
        return [
            ":red_heart:",
            ":pink_heart:",
            ":orange_heart:",
            ":yellow_heart:",
            ":green_heart:",
            ":blue_heart:",
            ":light_blue_heart:",
            ":purple_heart:",
            ":brown_heart:",
            ":black_heart:",
            ":grey_heart:",
            ":white_heart:",
            ":smiling_face_with_heart_eyes:",
            ":smiling_face_with_hearts:",
        ]
    if emojis_key == "thumb":
        return [
            ":face_with_steam_from_nose:",
            ":enraged_face:",
            ":angry_face:",
            ":face_with_symbols_on_mouth:",
        ]
    if emojis_key == "shock":
        return [":exploding_head:", ":face_with_open_mouth:", ":astonished_face:"]
    if emojis_key == "anger":
        return [
            ":face_with_steam_from_nose:",
            ":enraged_face:",
            ":angry_face:",
            ":face_with_symbols_on_mouth:",
        ]


def who_didnt_react(reacted_message, participants):
    reactors = participants.copy()
    for reaction in reacted_message.get("reactions", ""):
        actor = reaction.get("actor", "")
        reactors.remove(actor)
    return reactors


def get_trimmed_reacted_messages(all_reacted_messages, top_results, participants):
    trimmed_reacted_messages = []
    for message in all_reacted_messages[:top_results]:
        message["who_didnt_react"] = who_didnt_react(message, participants)
        trimmed_reacted_messages.append(message)
    return trimmed_reacted_messages


def main(
    data_to_parse,
    date_range_start,
    date_range_end,
    emojis_key,
    saveallreacts,
    saveallemojis,
):
    # Get messages and participants
    messages, participants = get_data_to_parse(
        data_to_parse, date_range_start, date_range_end
    )

    # Initialize reaction counter
    reaction_counter = initialise_counter_dict(participants)

    # Get all reacted messages
    all_reacted_messages = get_all_reacted_messages(messages)

    # Save all reacted messages or trim and save top results
    reaction_data = {}
    if saveallreacts:
        reaction_data["reacted_messages"] = all_reacted_messages
    else:
        top_results = 5
        trimmed_reacted_messages = get_trimmed_reacted_messages(
            all_reacted_messages, top_results, participants
        )
        reaction_data[f"top_{top_results}_reacted_messages"] = trimmed_reacted_messages

    # Find most and least reactive participant
    reaction_data["times_reacted"] = find_most_and_least_reactive_participant(
        all_reacted_messages, participants
    )

    # Get emojis to search
    emojis = get_emjois_to_search(emojis_key)

    # Find most likely to react with
    reaction_data[f"reaction_counter_{emojis_key}"] = find_most_likely_to_react_with(
        all_reacted_messages, emojis, reaction_counter
    )

    # Sum of reaction counter values
    reaction_data[f"reaction_counter_{emojis_key}_sum"] = sum(
        reaction_data[f"reaction_counter_{emojis_key}"].values()
    )

    # Save all emojis or get most common reactions
    if saveallemojis:
        reaction_data["emoji_counter"] = find_most_common_reaction(all_reacted_messages)

    # Find each participant's biggest fan
    reaction_data["fan_zone"] = find_each_participants_biggest_fan(all_reacted_messages)

    # Write results to file
    write_to_file("reactionator_results.json", reaction_data)


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
        "-e",
        "--emojis",
        type=str,
        help="The type of emoji you want to count",
        choices=["laugh", "heart", "thumb", "shock", "anger"],
        default="laugh",
    )
    parser.add_argument(
        "--saveallreacts",
        type=bool,
        default=False,
        help="Save all the reacted messages in the json",
    )
    parser.add_argument(
        "--saveallemojis",
        type=bool,
        default=False,
        help="Save all the emojis messages in the json",
    )
    args = parser.parse_args()

    main(
        initial_file_load(args.file, args.multichat),
        args.drstart,
        args.drend,
        args.emojis,
        args.saveallreacts,
        args.saveallemojis,
    )
