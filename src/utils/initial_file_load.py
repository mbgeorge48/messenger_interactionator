import os


def initial_file_load(path):
    files_to_parse=[]
    if os.path.isfile(path):
        files_to_parse=[path]
    elif os.path.isdir(path):
        for file in os.listdir(path):
            if file.endswith(".json"):
                files_to_parse.append(os.path.join(path, file))
    return files_to_parse