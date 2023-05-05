import operator
import sys

from utils import get_data_to_parse, initial_file_load, write_to_file


def initialise_reaction_counter_dict(participants):
    reaction_counter = {}
    for participant in participants:
        reaction_counter[participant] = 0
    return reaction_counter


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


def main(data_to_parse, date_range_start, date_range_end):
    messages, participants = get_data_to_parse(
        data_to_parse, date_range_start, date_range_end
    )
    reaction_counter = initialise_reaction_counter_dict(participants)

    reaction_data = {}
    reaction_data["reacted_messages"] = get_all_reacted_messages(messages)
    reaction_data["times_reacted"] = find_most_and_least_reactive_participant(
        reaction_data["reacted_messages"], participants
    )
    reaction_data["reaction_counter"] = find_most_likely_to_react_with(
        reaction_data["reacted_messages"], ["😅", "😂", "🤣", "😆"], reaction_counter
    )
    reaction_data["emoji_counter"] = find_most_common_reaction(
        reaction_data["reacted_messages"]
    )
    reaction_data["fan_zone"] = find_each_participants_biggest_fan(
        reaction_data["reacted_messages"]
    )
    write_to_file("reactionator_results.json", reaction_data)

    # Pull of the most/least reactive person
    # Run with the common emojis (laugh(all types), shock, heart)

    # with open('react_results.json', 'w') as f:
    #     json.dump(list_of_stuff, f, indent=4, separators=(',', ': '), ensure_ascii=False)


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
