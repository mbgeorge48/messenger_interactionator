import datetime
from utils import encode_string


def process_message_data(message):
    if message.get("content"):
        message['content'] = encode_string(message.get('content'))
    if message.get("bumped_message_metadata") and message.get("bumped_message_metadata").get("bumped_message") :
        message["bumped_message_metadata"]["bumped_message"] = encode_string(message.get('bumped_message_metadata').get("bumped_message"))
    if message.get("reactions"):
        for reaction in message.get("reactions"):
            reaction["reaction"] = encode_string(reaction.get('reaction'))
    if message.get("audio_files"):
        message["audio"] = message.pop("audio_files")
    message["timestamp_converted"] = datetime.datetime.fromtimestamp(message['timestamp_ms']/1000).strftime('%Y-%m-%d %H:%M:%S')

    return message
