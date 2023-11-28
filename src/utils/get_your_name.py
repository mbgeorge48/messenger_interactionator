from .load_json import load_json


"""
Usage
create a file in the root of the project called `your_name.json`
And populate it with something like:
["Gregory Biscuit"]
"""


def get_your_name():
    return load_json("your_name.json")
