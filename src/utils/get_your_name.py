from .load_json import load_json


def get_your_name():
    """
    Usage
    create a file in the root of the project called `your_name.json`
    And populate it with something like:
    ["Gregory Biscuit"]
    """
    return load_json("your_name.json")
