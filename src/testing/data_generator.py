import datetime
import json
import operator
import random
import emoji
import lorem
import requests


def generate_participant(*, index, realish):
    first_names = [
        "Greg",
        "Wallace",
        "Jerry",
        "Clive",
        "Ivan",
        "Bernard",
        "Otis",
        "Eugene",
    ]
    last_names = [
        "Biscuit",
        "Strong",
        "Whimma",
        "Smith",
        "Hagraven",
        "Potter",
        "Hunter",
        "Madri",
    ]
    if realish:
        full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
    else:
        full_name = f"user-{index}"
    return full_name


def generate_message_content(*, realish):
    if realish:
        content = requests.get(
            "https://icanhazdadjoke.com/", headers={"Accept": "text/plain"}
        ).content.decode()
    else:
        content = lorem.get_sentence(count=1, comma=(0, 2), word_range=(4, 8), sep=" ")
    return content


def generate_reaction(*, realish, participant):
    if not realish:
        valid_emoji = False
        while not valid_emoji:
            reaction = json.loads(
                requests.get(
                    "https://emojihub.yurace.pro/api/random/category/food-and-drink"
                ).content.decode()
            )
            # I find the food-and-drink category more reliable to convert
            emoji_name = emoji.emojize(f':{reaction.get("name").replace(" ","_")}:')

            if emoji.is_emoji(emoji_name):
                valid_emoji = True
    else:
        emoji_name = random.choice["🤡", "😆", "😎", "🤩"]

    return {"reaction": emoji_name, "actor": participant}


def generate_media(*, unix_timestamp):
    return {
        "uri": "random/file/location",
        "creation_timestamp": unix_timestamp,
    }


def generate_timestamp():
    year = 2020
    month = random.randint(1, 3)
    day = random.randint(1, 14)
    hour = random.randint(0, 23)
    minute = second = 0

    return datetime.datetime(year, month, day, hour, minute, second)


def generate_message_data(*, realish, participants):
    message_type = random.choices(["text", "media"], [10, 2])[0]
    has_reactions = random.choices([True, False], [2, 10])[0]

    message = {"sender_name": random.choice(participants)}

    timestamp = generate_timestamp()
    message["timestamp_ms"] = int(timestamp.timestamp() * 1000)

    if message_type == "text":
        message["content"] = generate_message_content(realish=realish)
    else:
        message[
            random.choice(["photos", "videos", "files", "audio_files", "gifs"])
        ] = generate_media(unix_timestamp=int(timestamp.timestamp()))

    if has_reactions:
        message["reactions"] = []
        max = len(participants)
        for _ in range(random.randint(1, int(max))):
            message["reactions"].append(
                generate_reaction(
                    realish=realish, participant=random.choice(participants)
                )
            )

    message["timestamp_converted"] = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    return message


def generate_title():
    return


if __name__ == "__main__":
    num_participants = int(input("number of participants => "))
    num_messages = int(input("number of messages => "))
    real_messages = input("use realish looking data (y/n) => ")

    if real_messages == "y":
        real_messages = True
    else:
        real_messages = False

    participants = []
    i = 0
    while i < num_participants:
        participants.append(generate_participant(index=i, realish=real_messages))
        list(dict.fromkeys(participants))
        i = len(participants)

    generated_data = {
        "participants": [{"name": participant} for participant in participants],
        "messages": [
            generate_message_data(realish=real_messages, participants=participants)
            for _ in range(num_messages)
        ],
        "title": "Sample Message Data",
    }

    messages = generated_data["messages"]
    sorted_messages = sorted(messages, key=operator.itemgetter("timestamp_ms"))
    generated_data["messages"] = sorted_messages

    with open("message_1.json", "w") as f:
        json.dump(
            generated_data,
            f,
            indent=4,
            separators=(",", ": "),
            ensure_ascii=False,
        )
