import json
import re
import collections
import datetime
import sys
import os
import operator

from utils import get_data_to_parse, initial_file_load, write_to_file

YOUR_NAME = "Matt George"


def get_all_reacted_messages(messages, min_reactions_length=0):
    all_reacted_messages=[]
    for message in messages:
        if "reactions" in message and len(message["reactions"])>min_reactions_length:
            message["reactions_length"]=len(message["reactions"])
            all_reacted_messages.append(message)
    return sorted(all_reacted_messages, key=operator.itemgetter('reactions_length'), reverse=True)


def find_most_and_least_reactive_participant(all_reacted_messages, participants):
    times_reacted={}
    for participant in participants:
        times_reacted[participant]=0
        for message in all_reacted_messages:
            for reaction in message["reactions"]:
                if reaction["actor"] == participant:
                    times_reacted[participant]=times_reacted[participant]+1

    times_reacted = dict(sorted(times_reacted.items(), key=lambda item: item[1],reverse=True))
    return times_reacted


def find_most_likely_to_react_with(all_reacted_messages, participants, emojis):
    return ""


def main(data_to_parse):
    messages, participants=get_data_to_parse(data_to_parse)
    reaction_data={}
    reaction_data['reacted_messages'] = get_all_reacted_messages(messages)
    reaction_data['times_reacted']=find_most_and_least_reactive_participant(reaction_data['reacted_messages'], participants)
    write_to_file("test.json", reaction_data)

    # Pull of the most/least reactive person
    # Run with the common emojis (laugh(all types), shock, heart)

    # with open('react_results.json', 'w') as f:
    #     json.dump(list_of_stuff, f, indent=4, separators=(',', ': '), ensure_ascii=False)


if __name__ == '__main__':
    if len(sys.argv)>1:
        main(initial_file_load(sys.argv[1]))
    else:
        print('Missing path to file')