import time
import datetime
import json
import re

YOUR_NAME = "Matt George"


class nickname_message():
    def __init__(self, timestamp, setter, msg_content):
        self.timestamp = timestamp
        self.setter = setter
        self.msg_content = msg_content


class nickname_event():
    def __init__(self, setter, settie, timestamp, nickname):
        self.setter = setter
        self.settie = settie
        # self.timestamp_formated = time.ctime(timestamp)
        self.timestamp_formated = datetime.datetime.utcfromtimestamp(
            timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
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
    participants = list()
    nickname_list = list()
    processed_nicknames = list()
    processed_participants = dict()

    def __init__(self):
        welcome_message = "Hello and welcome to the nickname parser"
        print(
            f"{'#'*(len(welcome_message))}\n{welcome_message}\n{'#'*(len(welcome_message))}")
        self.load_json_export()
        self.get_participant_names()
        self.get_all_nickname_updates()
        self.parse_nickname_messages()

        for person in self.participants:
            print(f"Processing {person}")
            persons_nicknames = list()
            for ne in self.processed_nicknames:
                if ne.settie == person:
                    persons_nicknames.append(self.process_participants(
                        person, ne))
            self.processed_participants[person] = {
                "Nicknames": persons_nicknames,
                "Number of nicknames": len(persons_nicknames)
            }

        print(json.dumps(self.processed_participants, sort_keys=True, indent=4))
        with open('result.json', 'w') as fp:
            json.dump(self.processed_participants, fp, indent=4,
                      separators=(',', ': '), sort_keys=True)

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
                    self.nickname_list.append(nickname_message(
                        message['timestamp_ms'], message['sender_name'], message['content']))
            except:
                pass

    def parse_nickname_messages(self):
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

            self.processed_nicknames.append(
                nickname_event(setter, settie, event.timestamp, nickname))

    def someone_set_your_nickname(self, message):
        settie = YOUR_NAME
        message_split = message.split()
        split = message_split.index("to")
        while message_split[split-1] != "nickname":
            message_split.remove("to")
            split = message_split.index("to")
        nickname = " ".join(message_split[split+1:])
        return settie, nickname[:-1]

    def someone_set_their_own_nickname(self, message, setter):
        settie = setter
        message_split = message.split()

        split = message_split.index("to")
        while message_split[split-1] != "nickname":
            message_split.remove("to")
            split = message_split.index("to")
        nickname = " ".join(message_split[split+1:])
        return settie, nickname[:-1]

    def set_someones_nickname(self, message):
        message_split = message.split()
        split = message_split.index("for")
        settie = message_split[split+1] + " " + message_split[split+2]

        nickname = " ".join(message_split[split+1:])
        return settie, nickname[nickname.find(settie + " to "):].replace(settie + " to ", "")[:-1]

    def process_participants(self, person, ne):
        this_event = dict()

        this_event["Nickname"] = ne.nickname
        this_event["Setter"] = ne.setter
        this_event["Timestamp"] = ne.timestamp_formated
        return this_event

        # need the format to look something like this
        # {
        # <name>:
        # <nickname>:
        # timestamp: <timestamp>
        # setter: <setter>
        # }


test = process_nicknames()
