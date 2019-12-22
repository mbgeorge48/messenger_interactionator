import time
import json
import re

YOUR_NAME = "Matt George"


class nickname_event():
    def __init__(self, timestamp, setter, msg_content):
        self.timestamp = timestamp
        self.setter = setter
        self.msg_content = msg_content


class nickname():
    def __init__(self, setter, settie, timestamp, nickname):
        self.setter = setter
        self.settie = settie
        self.timestamp_formated = time.ctime(timestamp)
        self.nickname = nickname


class participant():
    def __init__(self, name, setter, timestamp, nicknames):
        self.name = name
        self.setter = setter
        self.timestamp = timestamp
        self.timestamp_formated = time.ctime(timestamp)
        self.nicknames = nicknames


class process_nicknames():
    FILENAME = "message.json"
    json_string = None
    participants = list()  # Will contain a list of participant objects
    nickname_list = list()

    def __init__(self):
        welcome_message = "Hello and welcome to the nickname parser"
        print(
            f"{'#'*(len(welcome_message))}\n{welcome_message}\n{'#'*(len(welcome_message))}")
        self.load_json_export()
        self.get_participant_names()
        self.get_all_nickname_updates()
        self.parse_nickname_events()

    def load_json_export(self):
        with open(self.FILENAME) as json_data:
            self.json_string = json.load(json_data)

    def get_participant_names(self):
        for name in self.json_string["participants"]:
            self.participants.append(name['name'])

    def get_all_nickname_updates(self):
        main_pattern = '^.*?set (his own|her own|the|your) nickname.*?$'

        for message in self.json_string['messages']:
            try:  # Need to catch as I found that not all messages have content
                if re.match(main_pattern, message["content"]) is not None:
                    self.nickname_list.append(nickname_event(
                        message['timestamp_ms'], message['sender_name'], message['content']))
            except:
                pass

        # for event in self.nickname_list:
            # print(event.msg_content)

    def parse_nickname_events(self):
        # Need to split the message content up, chuck everything before "for" in the bin

        nickname_patterns = [  # Need one for one's you set for yourself
            "^.*?set your nickname to .*?",
            "^You set the nickname for .*?",
            "^.*?set (his own|her own) nickname to .*?",
            "^.*?set the nickname for .*?"
        ]
        for event in self.nickname_list:
            message = event.msg_content
            setter = event.setter
            if re.match(nickname_patterns[0], message) is not None:
                settie, nickname = self.someone_set_your_nickname(message)
            elif re.match(nickname_patterns[1], message) is not None or re.match(nickname_patterns[3], message) is not None:
                settie, nickname = self.set_someones_nickname(message)
            elif re.match(nickname_patterns[2], message) is not None:
                settie, nickname = self.someone_set_their_own_nickname(
                    message, setter)

            print(setter, settie, nickname, event.timestamp)

    def someone_set_your_nickname(self, message):
        settie = YOUR_NAME
        message_split = message.split()
        split = message_split.index("to")
        while split in message_split:
            if message_split[split-1] != "nickname":
                message_split.remove("to")
            else:
                break
        nickname = " ".join(message_split[split+1:])
        return settie, nickname[:-1]

    def someone_set_their_own_nickname(self, message, setter):
        settie = setter
        message_split = message.split()

        split = message_split.index("to")
        while split in message_split:
            if message_split[split-1] != "nickname":
                message_split.remove("to")
            else:
                break
        nickname = " ".join(message_split[split+1:])
        return settie, nickname[:-1]

    def set_someones_nickname(self, message):
        message_split = message.split()
        split = message_split.index("for")
        settie = message_split[split+1] + " " + message_split[split+2]
        nickname = " ".join(message_split[split+1:])
        return settie, nickname[nickname.find(settie + " to "):].replace(settie + " to ", "")[:-1]


test = process_nicknames()
