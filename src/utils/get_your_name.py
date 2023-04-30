from .load_json import load_json


def get_your_name():
    return load_json('your_name.json').name