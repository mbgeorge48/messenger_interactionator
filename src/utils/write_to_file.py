import json


def write_to_file(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4, separators=(',', ': '), ensure_ascii=False)
