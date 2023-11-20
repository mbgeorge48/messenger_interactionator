import emoji


def encode_string(string, emojize=False):
    new_string = string
    for ecoding in ["latin1", "utf8", "utf-16", "iso-8859-1"]:
        try:
            new_string = string.encode(ecoding).decode("utf8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
    if not emojize:
        new_string = emoji.demojize(new_string)
    else:
        new_string = emoji.emojize(new_string)
    return new_string
