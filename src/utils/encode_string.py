def encode_string(string):
    try:
        return string.encode("latin1").decode("utf8")
    except (UnicodeEncodeError, UnicodeDecodeError) as e:
        print(f"Failed to encode {string}: \t{e}")
        return string
