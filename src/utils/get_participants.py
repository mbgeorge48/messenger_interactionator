def get_participants(*, json_string):
    participants = []
    for name in json_string:
        participants.append(name["name"])
    return participants


def initialise_participants_dict(*, participants, initialiser):
    return dict.fromkeys(participants, initialiser)
