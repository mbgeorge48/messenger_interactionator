import utils

# def multi_chat_searching(data_to_parse)
# maybe need to change data_to_parse in the parent to say it's a list of dirs to scan
# the combined messages object will be huge

# def date_filter(messages, date_range):
# convert the range to the last day of the month specified
# if the date of the last message is outside the range AND the date of the first message is outside the range return none
# if only one is out of range then you need to go through and check each message
    # build a list of messages to return
# if one side is none then only bracket one side

# Date range needs to look like date_range_start="2023-04", date_range_end="2022-04"}
def get_data_to_parse(data_to_parse, date_range_start=None, date_range_end=None):
    # convert the date ranges into a date range dict
    data = []
    for file in data_to_parse:
        data.append(utils.read_message_file(file))
    participants = messages = []
    for entry in data:
        participants = participants + utils.get_participants(entry["participants"])
        # if date_range:
            # call filter function
            # messages = messages + date_filter_response
        messages = messages + entry["messages"]
    participants = list(dict.fromkeys(participants))
    return messages, participants
