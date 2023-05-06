import os

import utils


def multi_chat_searching(data_to_parse):
    chats_to_read = utils.load_json(data_to_parse[0])
    print(chats_to_read)
    for dir in chats_to_read:
        for file in dir:
            print(file)


def initial_file_load(path, multi_chat_search=False):
    files_to_parse = []
    if os.path.isfile(path):
        if not multi_chat_search:
            files_to_parse = [path]
        else:
            dirs_to_parse = utils.load_json(path)
            for dir in dirs_to_parse:
                for file in os.listdir(dir):
                    if file.endswith(".json"):
                        files_to_parse.append(os.path.join(dir, file))
    elif os.path.isdir(path):
        for file in os.listdir(path):
            if file.endswith(".json"):
                files_to_parse.append(os.path.join(path, file))
    return files_to_parse
