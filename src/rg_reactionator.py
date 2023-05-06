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
        if "reactions" in message and len(message["reactions"]) > min_reactions_length:
            message["reactions_length"] = len(message["reactions"])
            all_reacted_messages.append(message)
    return sorted(
        all_reacted_messages, key=operator.itemgetter("reactions_length"), reverse=True
    )


def find_most_and_least_reactive_participant(all_reacted_messages, participants):
    times_reacted = {}
    for participant in participants:
        times_reacted[participant] = 0
        for message in all_reacted_messages:
            for reaction in message["reactions"]:
                if reaction["actor"] == participant:
                    times_reacted[participant] += 1

    times_reacted = dict(
        sorted(times_reacted.items(), key=lambda item: item[1], reverse=True)
    )
    return times_reacted


def find_most_likely_to_react_with(all_reacted_messages, emojis, reaction_counter):
    for message in all_reacted_messages:
        for reaction in message["reactions"]:
            if reaction["reaction"] in emojis:
                try:
                    reaction_counter[reaction["actor"]] += 1
                except KeyError:
                    reaction_counter[reaction["actor"]] = 0
                    reaction_counter[reaction["actor"]] += 1

    return dict(
        sorted(reaction_counter.items(), key=lambda item: item[1], reverse=True)
    )


def find_most_common_reaction(all_reacted_messages):
    emoji_counter = {}
    for message in all_reacted_messages:
        for reaction in message["reactions"]:
            try:
                emoji_counter[reaction["reaction"]] += 1
            except KeyError:
                emoji_counter[reaction["reaction"]] = 0
                emoji_counter[reaction["reaction"]] += 1

    return dict(sorted(emoji_counter.items(), key=lambda item: item[1], reverse=True))


def find_each_participants_biggest_fan(all_reacted_messages):
    fan_zone = {}
    for message in all_reacted_messages:
        try:
            fan_zone[message["sender_name"]]
        except KeyError:
            fan_zone[message["sender_name"]] = {}
        for reaction in message["reactions"]:
            try:
                fan_zone[message["sender_name"]][reaction["actor"]] += 1
            except KeyError:
                fan_zone[message["sender_name"]][reaction["actor"]] = 0
                fan_zone[message["sender_name"]][reaction["actor"]] += 1

    for participant in fan_zone:
        fan_zone[participant] = dict(
            sorted(
                fan_zone[participant].items(), key=lambda item: item[1], reverse=True
            )
        )
    return fan_zone


def get_emjois_to_search(emojis_key):
    if emojis_key == "laugh":
        return ["😅", "😂", "🤣", "😆"]
    if emojis_key == "heart":
        return ["😍", "❤", "💜", "💗", "🥰", "💛", "💙", "💚"]
    if emojis_key == "thumb":
        return ["👍", " 👍🏻" ",👍🏾", "👍🏽", "👍🏼", "👍🏿"]
    if emojis_key == "shock":
        return ["😲", "🤯", "😮"]
    if emojis_key == "anger":
        return ["🤬", "😠"]


def main(
    data_to_parse,
    date_range_start,
    date_range_end,
    emojis_key,
    saveallreacts,
    saveallemojis,
):
    messages, participants = get_data_to_parse(
        data_to_parse, date_range_start, date_range_end
    )
    reaction_counter = initialise_counter_dict(participants)

    reaction_data = {}
    all_reacted_messages = get_all_reacted_messages(messages)
    if saveallreacts:
        reaction_data["reacted_messages"] = all_reacted_messages
    reaction_data["times_reacted"] = find_most_and_least_reactive_participant(
        all_reacted_messages, participants
    )
    emojis = get_emjois_to_search(emojis_key)
    reaction_data["reaction_counter"] = find_most_likely_to_react_with(
        all_reacted_messages, emojis, reaction_counter
    )
    if saveallemojis:
        reaction_data["emoji_counter"] = find_most_common_reaction(all_reacted_messages)
    reaction_data["fan_zone"] = find_each_participants_biggest_fan(all_reacted_messages)
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
        help="Save all the reacted messages in the json",
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
