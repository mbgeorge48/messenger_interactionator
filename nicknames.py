import time
import json
import re

YOUR_NAME = "MG"


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
        # Need to split it out so I can get the settie and the actual nickname out
        regex_pattern_a = "^.*? for .*? to .*?"
        # Need to split the message content up, chuck everything before "for" in the bin

        nickname_patterns = [  # Need one for one's you set for yourself
            "^.*?set your nickname to .*?",
            "^You set the nickname for .*?",
            "^.*?set (his own|her own) nickname to .*?",
            "^.*?set the nickname for .*?"
        ]
        for event in self.nickname_list:
            message_split = event.msg_content.split()
            if re.match(nickname_patterns[0], event.msg_content) is not None:
                self.someone_set_your_nickname(message_split)
            if re.match(nickname_patterns[1], event.msg_content) is not None:
                self.you_set_someones_nickname(message_split)
            if re.match(nickname_patterns[2], event.msg_content) is not None:
                self.someone_set_their_own_nickname(message_split)
            if re.match(nickname_patterns[3], event.msg_content) is not None:
                self.someone_set_someones_nickname(message_split)

        # for event in self.nickname_list:
        #     print(event.msg_content)
        #     message_split = event.msg_content.split()
        #     if "set the nickname for" in message_split:
        #         split = message_split.index("set the nickname for")
        #         print(split, len(message_split))
        #         if split > len(message_split):
        #             settie = YOUR_NAME
        #         else:
        #             settie = message_split[split+1] + \
        #                 " " + message_split[split+2]
        #         split = message_split.index("to")
        #         nickname = " ".join(message_split[split+1:])
        #     print(settie, nickname[nickname.find(
        #         settie + " to "):].replace(settie + " to ", "")[:-1])

    def someone_set_your_nickname(self, message_split):
        print("a")

    def you_set_someones_nickname(self, message_split):
        split = message_split.index("for")
        settie = message_split[split+1] + " " + message_split[split+2]
        nickname = " ".join(message_split[split+1:])
        print(settie, "===", nickname[nickname.find(
            settie + " to "):].replace(settie + " to ", "")[:-1])

    def someone_set_their_own_nickname(self, message_split):
        print("c")

    def someone_set_someones_nickname(self, message_split):
        split = message_split.index("for")
        settie = message_split[split+1] + " " + message_split[split+2]
        nickname = " ".join(message_split[split+1:])
        print(settie, "===", nickname[nickname.find(
            settie + " to "):].replace(settie + " to ", "")[:-1])


test = process_nicknames()
